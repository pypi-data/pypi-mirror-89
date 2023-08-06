#include "mm.h"

void mm_forward(
    const torch::Tensor& mata,
    const torch::Tensor& matb,
    torch::Tensor& matc,
    const torch::Tensor& one,
    const torch::Tensor& zero) {
    const auto M = matc.size(0);
    const auto N = matc.size(1);
    const auto K = mata.size(1);

    const float* maptr = mata.data<float>();
    const float* mbptr = matb.data<float>();
    float* mcptr = matc.data<float>();
    const float* oneptr = one.data<float>();
    const float* zeroptr = zero.data<float>();
	cublasHandle_t handle;
    checkCublasErr(cublasCreate(&handle));
    checkCublasErr(cublasSgemm(handle, CUBLAS_OP_N, CUBLAS_OP_N,
                N, M, K, oneptr, mbptr, N, maptr, K, zeroptr, mcptr, N));
}

void mm_backward(
    const torch::Tensor& mata,
    const torch::Tensor& matb,
    const torch::Tensor& gradc,
    torch::Tensor& grada,
    torch::Tensor& gradb,
    const torch::Tensor& one,
    const torch::Tensor& zero) {

    const auto M = gradc.size(0);
    const auto N = gradc.size(1);
    const auto K = mata.size(1);

    const float* maptr = mata.data<float>();
    const float* mbptr = matb.data<float>();
    const float* gcptr = gradc.data<float>();
    float* gaptr = grada.data<float>();
    float* gbptr = gradb.data<float>();
    const float* oneptr = one.data<float>();
    const float* zeroptr = zero.data<float>();
	cublasHandle_t handle;
    checkCublasErr(cublasCreate(&handle));
    //checkCublasErr(cublasSgemm(handle, CUBLAS_OP_N, CUBLAS_OP_N,
    //            N, M, K, oneptr, mbptr, N, maptr, K, zeroptr, mcptr, N));
    // a: m*k   ga: m*k
    // b: k*n   bt: n*k
    // c: m*n   gc: m*n

    // a * b = c
    // gc * bt = ga, newk = n, newm = m, newn = k, b->bt

    // bt*at=ct
    // a*b=c, c->ct
    // b=bt, d = bt, a * d = c==>dt * at = ct==>b * at = ct

    checkCublasErr(cublasSgemm(handle, CUBLAS_OP_T, CUBLAS_OP_N,
                K, M, N, oneptr, mbptr, N, gcptr, N, zeroptr, gaptr, K));
    checkCublasErr(cublasSgemm(handle, CUBLAS_OP_N, CUBLAS_OP_T,
                N, K, M, oneptr, gcptr, N, maptr, K, zeroptr, gbptr, N));
}

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
  m.def("mm_forward", &mm_forward, "mm forward (CUDA)");
  m.def("mm_backward", &mm_backward, "mm backward (CUDA)");
}

