#include "lstm.h"
#include "lstm_kernel.h"

void lstm_forward(
    const std::vector<torch::Tensor>& inputs,
    std::vector<torch::Tensor>& outputs,
    const torch::Tensor& one,
    const torch::Tensor& zero) {

    const torch::Tensor& x0 = inputs[0];
    const torch::Tensor& h0 = inputs[1];
    const torch::Tensor& c0 = inputs[2];
    const torch::Tensor& wx = inputs[3];
    const torch::Tensor& wh = inputs[4];
    const torch::Tensor& bias = inputs[5];
    const torch::Tensor& ln_gamma = inputs[6];
    const torch::Tensor& ln_beta = inputs[7];

    torch::Tensor& xbuf = outputs[0];
    torch::Tensor& hbuf = outputs[1];
    torch::Tensor& hn = outputs[2];
    torch::Tensor& cn = outputs[3];
    torch::Tensor& ifog = outputs[4];
    torch::Tensor& ym = outputs[5];
    torch::Tensor& ln_xmu = outputs[6];
    torch::Tensor& ln_xivar = outputs[7];

    const auto seq_len = x0.size(0);
    const auto batch_size = x0.size(1);
    const auto input_size = x0.size(2);
	const auto num_layers = h0.size(0);
    const auto hidden_size = h0.size(2);

    const float* inputptr = x0.data<float>();
    const float* h0ptr = h0.data<float>();
    const float* c0ptr = c0.data<float>();
    const float* wxptr = wx.data<float>();
    const float* whptr = wh.data<float>();
    const float* biasptr = bias.data<float>();
    const float* ln_gammaptr = ln_gamma.data<float>();
    const float* ln_betaptr = ln_beta.data<float>();
    float* xbufptr = xbuf.data<float>();
    float* hbufptr = hbuf.data<float>();
    float* hnptr = hn.data<float>();
    float* cnptr = cn.data<float>();
    float* ifogptr = ifog.data<float>();
    float* outputptr = ym.data<float>();
    float* ln_xmuptr = ln_xmu.data<float>();
    float* ln_xivarptr = ln_xivar.data<float>();
    const float* oneptr = one.data<float>();
    const float* zeroptr = zero.data<float>();

    //double dur;
    //clock_t start,end;
    //start = clock();
	cublasHandle_t handle;
    checkCublasErr(cublasCreate(&handle));
    //end = clock();
    //dur = (double)(end - start);
    //printf("cublasCreate use Time:%f\n",(dur/CLOCKS_PER_SEC));

    // TODO wyr pay attention to wx shape change
    int wxidx[num_layers];
    wxidx[0] = input_size;
    for (int l = 0; l < num_layers - 1; l++) {
        wxidx[l + 1] = hidden_size;
    }
    int wxoffset[num_layers];
    wxoffset[0] = 0;
    for (int l = 0; l < num_layers - 1; l++) {
        wxoffset[l + 1] = wxoffset[l] + wxidx[l] * wxidx[l + 1] * 4;
    }

    for (int l = 0; l < num_layers; l++) {
        //start = clock();
        const float* ln_gamma_x = ln_gammaptr + l * hidden_size * 4 * 2;
        const float* ln_gamma_h = ln_gammaptr + l * hidden_size * 4 * 2 + hidden_size * 4;
        const float* ln_beta_x = ln_betaptr + l * hidden_size * 4 * 2;
        const float* ln_beta_h = ln_betaptr + l * hidden_size * 4 * 2 + hidden_size * 4;
        float* ln_xmu_x = ln_xmuptr + l * seq_len * batch_size * hidden_size * 4 * 2;
        float* ln_xmu_h = ln_xmuptr + l * seq_len * batch_size * hidden_size * 4 * 2 + seq_len * batch_size * hidden_size * 4;
        float* ln_xivar_x = ln_xivarptr + l * seq_len * batch_size * 2;
        float* ln_xivar_h = ln_xivarptr + l * seq_len * batch_size * 2 + seq_len * batch_size;

        //int err = cudaDeviceSynchronize();
        //fprintf(stderr, "%s %d, before sync, l: %d, err: %d\n", __FILE__, __LINE__, l, err);
        const float* xdata = (l == 0 ? inputptr : (outputptr + (l - 1) * seq_len * batch_size * hidden_size));
        const float* wxdata = wxptr + wxoffset[l];
        checkCublasErr(cublasSgemm(handle, CUBLAS_OP_N, CUBLAS_OP_N,
                    hidden_size * 4, seq_len * batch_size, wxidx[l],
                    oneptr, wxdata, hidden_size * 4, xdata, wxidx[l], zeroptr, xbufptr, hidden_size * 4));
        //err = cudaDeviceSynchronize();
        //fprintf(stderr, "%s %d, after sync, l: %d, err: %d\n", __FILE__, __LINE__, l, err);

        //end = clock();
        //dur = (double)(end - start);
        //printf("layer gemm use Time:%f\n",(dur/CLOCKS_PER_SEC));    

        //start = clock();

        int blockSize = DEFAULTWARPNUM * WARPSIZE;
        int gridSize = seq_len * batch_size;
        ppl3::cuda::layernorm<float><<<gridSize, blockSize>>>(
                hidden_size * 4, (const float*)xbufptr, ln_gamma_x, ln_beta_x, ln_xmu_x, ln_xivar_x, xbufptr);
        //err = cudaDeviceSynchronize();

        //end = clock();
        //dur = (double)(end - start);
        //printf("layer ln use Time:%f\n",(dur/CLOCKS_PER_SEC));    

        //int len = seq_len * batch_size * hidden_size * 4;
        //float hostbuf[len];
        //cudaMemcpy(hostbuf, xbufptr, len * sizeof(float), cudaMemcpyDeviceToHost);
        //for (int i = 0; i < len; i++) {
        //    fprintf(stderr, "xbufptr[%d]: %lf\n", i, hostbuf[i]);
        //}

        bool hasbias = true;
        const float* biasdata = biasptr + l * (hidden_size * 4);
        const float* whdata = whptr + l * hidden_size * (hidden_size * 4);
        for (int s = 0; s < seq_len; s++) {
            //err = cudaDeviceSynchronize();
            //fprintf(stderr, "%s %d, before gemm, l: %d, s: %d, err: %d\n", __FILE__, __LINE__, l, s, err);

            const float* xbufdata = xbufptr + s * batch_size * (hidden_size * 4);
            const float* prehdata = (s == 0 ? (h0ptr + l * batch_size * hidden_size)
                    : (hnptr + (s - 1) * num_layers * batch_size * hidden_size + l * batch_size * hidden_size));
            const float* precdata = (s == 0 ? (c0ptr + l * batch_size * hidden_size)
                    : (cnptr + (s - 1) * num_layers * batch_size * hidden_size + l * batch_size * hidden_size));
            float* hdata = hnptr + s * num_layers * batch_size * hidden_size + l * batch_size * hidden_size;
            float* cdata = cnptr + s * num_layers * batch_size * hidden_size + l * batch_size * hidden_size;
            float* ifogdata = ifogptr + l * seq_len * batch_size * hidden_size * 4 + s * batch_size * hidden_size * 4;
            float* outputdata = outputptr + l * seq_len * batch_size * hidden_size + s * batch_size * hidden_size;
            //start = clock();
            //err = cudaDeviceSynchronize();

            //fprintf(stderr, "wh shape: %d %d %d, h shape: %d %d %d, hbuf shape: %d %d\n",
            //        wh.size(0), wh.size(1), wh.size(2), h.size(0), h.size(1), h.size(2), hbuf.size(0), hbuf.size(1));
            checkCublasErr(cublasSgemm(handle, CUBLAS_OP_N, CUBLAS_OP_N,
                        hidden_size * 4, batch_size, hidden_size,
                        oneptr, whdata, hidden_size * 4, prehdata, hidden_size, zeroptr, hbufptr, hidden_size * 4));

            //err = cudaDeviceSynchronize();
            //fprintf(stderr, "%s %d, after gemm, l: %d, s: %d, err: %d\n", __FILE__, __LINE__, l, s, err);
            //err = cudaDeviceSynchronize();
            //end = clock();
            //dur = (double)(end - start);
            //printf("seq gemm use time:%f\n",(dur/CLOCKS_PER_SEC));

            //start = clock();

            {
            float* ln_xmu_h_s = ln_xmu_h + s * batch_size * hidden_size * 4;
            float* ln_xivar_h_s = ln_xivar_h + s * batch_size;
            int blockSize = DEFAULTWARPNUM * WARPSIZE;
            int gridSize = batch_size;
            ppl3::cuda::layernorm<float><<<gridSize, blockSize>>>(
                    hidden_size * 4, (const float*)hbufptr, ln_gamma_h, ln_beta_h, ln_xmu_h_s, ln_xivar_h_s, hbufptr);
            }
  
            //err = cudaDeviceSynchronize();
            //end = clock();
            //dur = (double)(end - start);
            //printf("seq ln use time:%f\n",(dur/CLOCKS_PER_SEC));

            //start = clock();

            //int len = batch_size * hidden_size * 4;
            //float hostbuf[len];
            //cudaMemcpy(hostbuf, hbufptr, len * sizeof(float), cudaMemcpyDeviceToHost);
            //for (int i = 0; i < len; i++) {
            //    fprintf(stderr, "hbufptr[%d]: %lf\n", i, hostbuf[i]);
            //}

            {
            dim3 blockSize = {DEFAULTWARPNUM * WARPSIZE, 1, 1};
            dim3 gridSize = {(hidden_size + blockSize.x - 1) / blockSize.x, batch_size, 1};
            ppl3::cuda::activation<float><<<gridSize, blockSize>>>(
                    batch_size, hidden_size, xbufdata , hbufptr, hasbias, biasdata,
                    prehdata, precdata, hdata, cdata, ifogdata, outputdata);
            }

            //err = cudaDeviceSynchronize();
            //end = clock();
            //dur = (double)(end - start);
            //printf("seq activation use time:%f\n",(dur/CLOCKS_PER_SEC));
        }
    }
}

void lstm_backward(
    const std::vector<torch::Tensor>& inputs,
    std::vector<torch::Tensor>& outputs,
    const torch::Tensor& one,
    const torch::Tensor& zero) {

    const torch::Tensor& x0 = inputs[0];
    const torch::Tensor& h0 = inputs[1];
    const torch::Tensor& c0 = inputs[2];
    const torch::Tensor& wx = inputs[3];
    const torch::Tensor& wh = inputs[4];
    const torch::Tensor& hn = inputs[5];
    const torch::Tensor& cn = inputs[6];
    const torch::Tensor& ifogbuf = inputs[7];
    const torch::Tensor& ym = inputs[8];
    const torch::Tensor& ln_gamma = inputs[9];
    const torch::Tensor& ln_xmu = inputs[10];
    const torch::Tensor& ln_xivar = inputs[11];

    torch::Tensor& dgatebuf = outputs[0];
    torch::Tensor& xbuf = outputs[1];
    torch::Tensor& hbuf = outputs[2];
    torch::Tensor& dy = outputs[3];
    torch::Tensor& dx = outputs[4];
    torch::Tensor& dh = outputs[5];
    torch::Tensor& dc = outputs[6];
    torch::Tensor& dwx = outputs[7];
    torch::Tensor& dwh = outputs[8];
    torch::Tensor& dbias = outputs[9];
    torch::Tensor& d_ln_gamma = outputs[10];
    torch::Tensor& d_ln_beta = outputs[11];

    const auto seq_len = x0.size(0);
    const auto batch_size = x0.size(1);
    const auto input_size = x0.size(2);
	const auto num_layers = h0.size(0);
    const auto hidden_size = h0.size(2);

    const float* x0ptr = x0.data<float>();
    const float* ifogptr = ifogbuf.data<float>();
    const float* ymptr = ym.data<float>();
    const float* h0ptr = h0.data<float>();
    const float* c0ptr = c0.data<float>();
    const float* hnptr = hn.data<float>();
    const float* cnptr = cn.data<float>();
    const float* wxptr = wx.data<float>();
    const float* whptr = wh.data<float>();
    const float* oneptr = one.data<float>();
    const float* zeroptr = zero.data<float>();
    const float* ln_gammaptr = ln_gamma.data<float>();
    const float* ln_xmuptr = ln_xmu.data<float>();
    const float* ln_xivarptr = ln_xivar.data<float>();
    float* dgatebufptr = dgatebuf.data<float>();
    float* xbufptr = xbuf.data<float>();
    float* hbufptr = hbuf.data<float>();
    float* dyptr = dy.data<float>();
    float* dxptr = dx.data<float>();
    float* dhptr = dh.data<float>();
    float* dcptr = dc.data<float>();
    float* dwxptr = dwx.data<float>();
    float* dwhptr = dwh.data<float>();
    float* dbiasptr = dbias.data<float>();
    float* ln_dgammaptr = d_ln_gamma.data<float>();
    float* ln_dbetaptr = d_ln_beta.data<float>();

	cublasHandle_t handle;
    checkCublasErr(cublasCreate(&handle));

    // TODO wyr pay attention to wx shape change
    int wxidx[num_layers + 1];
    wxidx[0] = input_size;
    for (int l = 0; l < num_layers; l++) {
        wxidx[l + 1] = hidden_size;
    }
    int wxoffset[num_layers + 1];
    wxoffset[0] = 0;
    int totalwx = 0;
    for (int l = 0; l < num_layers; l++) {
        totalwx += wxidx[l] * wxidx[l + 1] * 4;
        wxoffset[l + 1] = wxoffset[l] + wxidx[l] * wxidx[l + 1] * 4;
    }

    bool hasbias = true;
    cudaMemsetAsync(dxptr, 0, seq_len * batch_size * input_size * sizeof(float));
    cudaMemsetAsync(dwxptr, 0, totalwx * sizeof(float));
    cudaMemsetAsync(dwhptr, 0, num_layers * hidden_size * hidden_size * 4 * sizeof(float));
    cudaMemsetAsync(dbiasptr, 0, num_layers * hidden_size * 4 * sizeof(float));
    cudaMemsetAsync(ln_dgammaptr, 0, num_layers * hidden_size * 4 * 2 * sizeof(float));
    cudaMemsetAsync(ln_dbetaptr, 0, num_layers * hidden_size * 4 * 2 * sizeof(float));
    for (int l = num_layers - 1; l >= 0; l--) {
        // layernorm
        const float* ln_gamma_x = ln_gammaptr + l * hidden_size * 4 * 2;
        const float* ln_gamma_h = ln_gammaptr + l * hidden_size * 4 * 2 + hidden_size * 4;
        float* ln_dgamma_x = ln_dgammaptr + l * hidden_size * 4 * 2;
        float* ln_dgamma_h = ln_dgammaptr + l * hidden_size * 4 * 2 + hidden_size * 4;
        float* ln_dbeta_x = ln_dbetaptr + l * hidden_size * 4 * 2;
        float* ln_dbeta_h = ln_dbetaptr + l * hidden_size * 4 * 2 + hidden_size * 4;

        // lstm
        const float* wxdata = wxptr + wxoffset[l];
        float* dwxdata = dwxptr + wxoffset[l];
        const float* whdata = whptr + l * hidden_size * hidden_size * 4;
        float* dwhdata = dwhptr + l * hidden_size * hidden_size * 4;
        float* dbiasdata = dbiasptr + l * hidden_size * 4;
        cudaMemsetAsync(dhptr, 0, batch_size * hidden_size * sizeof(float));
        cudaMemsetAsync(dcptr, 0, batch_size * hidden_size * sizeof(float));
        const float* xlayer = (l == 0 ? x0ptr : (ymptr + (l - 1) * seq_len * batch_size * hidden_size));
        float* dxlayer = (l == 0 ? dxptr : dyptr);
        for (int s = seq_len - 1; s >= 0; s--) {
            const float* cdata = cnptr + s * num_layers * batch_size * hidden_size + l * batch_size * hidden_size;
            const float* prehdata = (s == 0 ? (h0ptr + l * batch_size * hidden_size)
                    : (hnptr + (s - 1) * num_layers * batch_size * hidden_size + l * batch_size * hidden_size));
            const float* precdata = (s == 0 ? (c0ptr + l * batch_size * hidden_size)
                    : (cnptr + (s - 1) * num_layers * batch_size * hidden_size + l * batch_size * hidden_size));
            const float* ifogdata = ifogptr + l * seq_len * batch_size * hidden_size * 4 + s * batch_size * hidden_size * 4;
            const float* dydata = dyptr + s * batch_size * hidden_size;
            const float* xdata = xlayer + s * batch_size * wxidx[l];
            float* dxdata = dxlayer + s * batch_size * wxidx[l];
            {
            dim3 blockSize = {DEFAULTWARPNUM * WARPSIZE, 1, 1};
            dim3 gridSize = {(hidden_size + blockSize.x - 1) / blockSize.x, batch_size, 1};
            ppl3::cuda::activation_backward<float><<<gridSize, blockSize>>>(
                    batch_size, hidden_size, dydata, cdata, precdata, ifogdata,
                    dgatebufptr, dhptr, dcptr, hasbias, dbiasdata);
            }

            // layernorm
            const float* ln_xmu_x = ln_xmuptr + l * seq_len * batch_size * hidden_size * 4 * 2 +
                s * batch_size * hidden_size * 4;
            const float* ln_xmu_h = ln_xmuptr + l * seq_len * batch_size * hidden_size * 4 * 2 +
                seq_len * batch_size * hidden_size * 4 + s * batch_size * hidden_size * 4;
            const float* ln_xivar_x = ln_xivarptr + l * seq_len * batch_size * 2 + s * batch_size;
            const float* ln_xivar_h = ln_xivarptr + l * seq_len * batch_size * 2 + seq_len * batch_size + s * batch_size;
            {
            int blockSize = DEFAULTWARPNUM * WARPSIZE;
            int gridSize = batch_size;
            // xbufptr has seq_len blocks(for fp), bp only use the first block
            ppl3::cuda::layernorm_backward<float><<<gridSize, blockSize>>>(
                    hidden_size * 4, ln_gamma_x, ln_xmu_x, ln_xivar_x, dgatebufptr, ln_dgamma_x, ln_dbeta_x, xbufptr);
            }
            {
            int blockSize = DEFAULTWARPNUM * WARPSIZE;
            int gridSize = batch_size;
            ppl3::cuda::layernorm_backward<float><<<gridSize, blockSize>>>(
                    hidden_size * 4, ln_gamma_h, ln_xmu_h, ln_xivar_h, dgatebufptr, ln_dgamma_h, ln_dbeta_h, hbufptr);
            }
 
            // dwx += torch.matmul(x_t, d_gate)
            checkCublasErr(cublasSgemm(handle, CUBLAS_OP_N, CUBLAS_OP_T,
                        hidden_size * 4, wxidx[l], batch_size,
                        oneptr, xbufptr, hidden_size * 4, xdata, wxidx[l],
                        oneptr, dwxdata, hidden_size * 4));

            // dwh += torch.matmul(h_t, d_gate)
            checkCublasErr(cublasSgemm(handle, CUBLAS_OP_N, CUBLAS_OP_T,
                        hidden_size * 4, hidden_size, batch_size,
                        oneptr, hbufptr, hidden_size * 4, prehdata, hidden_size,
                        oneptr, dwhdata, hidden_size * 4));

            // dx = torch.matmul(d_gate, wx_t)
            checkCublasErr(cublasSgemm(handle, CUBLAS_OP_T, CUBLAS_OP_N,
                        wxidx[l], batch_size, hidden_size * 4,
                        oneptr, wxdata, hidden_size * 4, xbufptr, hidden_size * 4,
                        zeroptr, dxdata, wxidx[l]));

            // dh = torch.matmul(d_gate, wh_t)
            checkCublasErr(cublasSgemm(handle, CUBLAS_OP_T, CUBLAS_OP_N,
                        hidden_size, batch_size, hidden_size * 4,
                        oneptr, whdata, hidden_size * 4, hbufptr, hidden_size * 4,
                        zeroptr, dhptr, hidden_size));
        }
    }
}

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
  m.def("lstm_forward", &lstm_forward, "lstm forward (CUDA)");
  m.def("lstm_backward", &lstm_backward, "lstm backward (CUDA)");
}
