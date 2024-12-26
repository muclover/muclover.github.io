#!/bin/bash

ut_tests=(
    "cargo test -p ylong_http --lib --features huffman,http1_1,http2,tokio_base"
    "cargo test -p ylong_http --lib --features huffman,http1_1,http2,ylong_base"
    "cargo test -p ylong_http_client --lib --features async,http1_1,tokio_base"
    "cargo test -p ylong_http_client --lib --features async,http1_1,ylong_base"
    "cargo test -p ylong_http_client --lib --features async,http1_1,http2,tokio_base"
    "cargo test -p ylong_http_client --lib --features async,http1_1,http2,ylong_base"
    "cargo test -p ylong_http_client --lib --features async,http1_1,http2,tokio_base,c_openssl_3_0"
    "cargo test -p ylong_http_client --lib --features async,http1_1,http2,ylong_base,c_openssl_3_0"
)

all_tests=(
    "cargo test -p ylong_http --features huffman,http1_1,http2,tokio_base"
    "cargo test -p ylong_http --features huffman,http1_1,http2,ylong_base"
    "cargo test -p ylong_http_client --features async,http1_1,tokio_base"
    "cargo test -p ylong_http_client --features async,http1_1,ylong_base"
    "cargo test -p ylong_http_client --features async,http1_1,http2,tokio_base"
    "cargo test -p ylong_http_client --features async,http1_1,http2,ylong_base"
    "cargo test -p ylong_http_client --features async,http1_1,http2,tokio_base,c_openssl_3_0"
    "cargo test -p ylong_http_client --features async,http1_1,http2,ylong_base,c_openssl_3_0"
)

# 检查是否传入参数sdv
if [ $# -eq 1 ] && [ "$1" = "sdv" ]; then
    target_commands=("${all_tests[@]}")
else
    target_commands=("${ut_tests[@]}")
fi

for cmd in "${target_commands[@]}"; do
    echo "Executing: $cmd"
    $cmd
    if [ $? -ne 0 ]; then
        echo "Error occurred while executing: $cmd"
        exit 1
    fi
done


echo ""
echo "------------- Start Exec Clippy ----------"

ut_clippy=(
    "cargo clippy --tests -p ylong_http --lib --features huffman,http1_1,http2,tokio_base"
    "cargo clippy --tests -p ylong_http --lib --features huffman,http1_1,http2,ylong_base"
    "cargo clippy --tests -p ylong_http_client --lib --features async,http1_1,tokio_base"
    "cargo clippy --tests -p ylong_http_client --lib --features async,http1_1,ylong_base"
    "cargo clippy --tests -p ylong_http_client --lib --features async,http1_1,http2,tokio_base"
    "cargo clippy --tests -p ylong_http_client --lib --features async,http1_1,http2,ylong_base"
    "cargo clippy --tests -p ylong_http_client --lib --features async,http1_1,http2,tokio_base,c_openssl_3_0"
    "cargo clippy --tests -p ylong_http_client --lib --features async,http1_1,http2,ylong_base,c_openssl_3_0"
)

all_clippy=(
    "cargo clippy --tests -p ylong_http --features huffman,http1_1,http2,tokio_base"
    "cargo clippy --tests -p ylong_http --features huffman,http1_1,http2,ylong_base"
    "cargo clippy --tests -p ylong_http_client --features async,http1_1,tokio_base"
    "cargo clippy --tests -p ylong_http_client --features async,http1_1,ylong_base"
    "cargo clippy --tests -p ylong_http_client --features async,http1_1,http2,tokio_base"
    "cargo clippy --tests -p ylong_http_client --features async,http1_1,http2,ylong_base"
    "cargo clippy --tests -p ylong_http_client --features async,http1_1,http2,tokio_base,c_openssl_3_0"
    "cargo clippy --tests -p ylong_http_client --features async,http1_1,http2,ylong_base,c_openssl_3_0"
)

# 检查是否传入参数sdv
if [ $# -eq 1 ] && [ "$1" = "sdv" ]; then
    target_commands=("${all_clippy[@]}")
else
    target_commands=("${ut_clippy[@]}")
fi

for cmd in "${target_commands[@]}"; do
    echo "Executing: $cmd"
    $cmd
    if [ $? -ne 0 ]; then
        echo "Error occurred while executing: $cmd"
        exit 1
    fi
done