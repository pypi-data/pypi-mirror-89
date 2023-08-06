#include "ln.h"
#include "ln_kernel.h"
void ln_forward(
    const torch::Tensor& x,
    const torch::Tensor& gamma,
    const torch::Tensor& beta,
    torch::Tensor& xmu,
    torch::Tensor& xivar,
    torch::Tensor& y) {
    const auto M = x.size(0);
    const auto N = x.size(1);

    const float* xptr = x.data<float>();
    const float* gammaptr = gamma.data<float>();
    const float* betaptr = beta.data<float>();
    float* xmuptr = xmu.data<float>();
    float* xivarptr = xivar.data<float>();
    float* yptr = y.data<float>();

    int blockSize = DEFAULTWARPNUM * WARPSIZE;
    int gridSize = M;
    ppl3::cuda::layernorm<float><<<gridSize, blockSize>>>(N, xptr, gammaptr, betaptr, xmuptr, xivarptr, yptr);
}

void ln_backward(
    const torch::Tensor& gamma,
    const torch::Tensor& xmu,
    const torch::Tensor& xivar,
    const torch::Tensor& grady,
    torch::Tensor& dgamma,
    torch::Tensor& dbeta,
    torch::Tensor& gradx) {
    const auto M = grady.size(0);
    const auto N = grady.size(1);

    const float* gammaptr = gamma.data<float>();
    const float* xmuptr = xmu.data<float>();
    const float* xivarptr = xivar.data<float>();
    const float* gradyptr = grady.data<float>();
    float* dgammaptr = dgamma.data<float>();
    float* dbetaptr = dbeta.data<float>();
    float* gradxptr = gradx.data<float>();

    //int err = cudaDeviceSynchronize();
    //int len = M * N;
    //float hostbuf[len];
    //cudaMemcpy(hostbuf, xivarptr, len * sizeof(float), cudaMemcpyDeviceToHost);
    //for (int i = 0; i < len; i++) {
    //    fprintf(stderr, "xivar data[%d]: %lf\n", i, hostbuf[i]);
    //}

    int blockSize = DEFAULTWARPNUM * WARPSIZE;
    int gridSize = M;
    ppl3::cuda::layernorm_backward<float><<<gridSize, blockSize>>>(N, gammaptr, xmuptr, xivarptr, gradyptr, dgammaptr, dbetaptr, gradxptr);    
}

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
  m.def("ln_forward", &ln_forward, "ln forward (CUDA)");
  m.def("ln_backward", &ln_backward, "ln backward (CUDA)");
}

