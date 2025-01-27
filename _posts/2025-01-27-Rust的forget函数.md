---
title: Rust 中的 std::mem::forget 函数
tags: Archive Rust Basic
sidebar:
 nav: rust
aside:
 toc: true
---
## std::mem::forget 函数
为什么在转换为迭代器后，不会调用 drop 函数
- 因为在 into_iter 中使用了 `std::mem::forget` 函数

`into_iter` 函数将一个集合转换为一个迭代器，它会获取集合的所有权。
- 创建一个迭代器对象。
- 将集合的所有权转移到迭代器中。
- 防止集合的析构函数被自动调用（因为集合的所有权已经被转移）。

`std::mem::forget` 是 Rust 标准库中的一个函数，它的作用是防止 Rust 自动调用析构函数。具体来说：
- 当你调用 `forget(self)` 时，self 的所有权被“遗忘”，Rust 不会自动调用其析构函数。
- 这通常用于手动管理资源的生命周期，例如在实现自定义迭代器时。

函数原型
```rust
pub fn forget<T>(t: T)
```

使用场景，主要有三种：手动管理资源、与FFI进行交互、自定义迭代器

- **手动管理资源**

```rust
use std::mem::forget;
use std::ptr;

struct MyResource {
    data: *mut u8,
}

impl Drop for MyResource {
    fn drop(&mut self) {
        println!("Dropping MyResource");
        unsafe { ptr::drop_in_place(self.data); }
    }
}

fn main() {
    let resource = MyResource { data: Box::into_raw(Box::new(42)) };
    // 遗忘 resource，防止自动调用 Drop
    forget(resource);
    // 手动释放资源
    unsafe {
        println!("Manually dropping resource");
        Box::from_raw(resource.data);  // 调用 Box 的析构函数
    }
}
```
- **与 FFI 交互**：将资源传递给C代码时，防止 Rust 在外部的C代码仍然使用这些资源时自动释放它们。
```rust
use std::mem::forget;

struct MyResource {
    data: *mut u8,
}
impl Drop for MyResource {
    fn drop(&mut self) {
        println!("Dropping MyResource");
        // 释放资源
    }
}
fn pass_to_c(resource: MyResource) {
    // 将资源传递给 C 代码
    unsafe {
        // 假设有一个 C 函数接收资源
        // c_function(resource.data);
    }
    // 遗忘资源，防止自动调用 Drop
    forget(resource);
}
fn main() {
    let resource = MyResource { data: Box::into_raw(Box::new(42)) };
    pass_to_c(resource);
}
```

- **自定义迭代器**
```rust
use std::mem::forget;

struct MyCollection {
    data: Vec<i32>,
}
impl Drop for MyCollection {
    fn drop(&mut self) {
        println!("Dropping MyCollection");
    }
}
struct MyIterator {
    data: Vec<i32>,
    index: usize,
}
impl MyCollection {
    fn into_iter(self) -> MyIterator {
        let iter = MyIterator {
            data: self.data,
            index: 0,
        };
        // 遗忘原始集合，防止自动调用 Drop
        forget(self);
        iter
    }
}
fn main() {
    let collection = MyCollection { data: vec![1, 2, 3] };
    let iter = collection.into_iter();

    for item in iter {
        println!("{}", item);
    }
}
```

forget 的主要作用是防止 Drop 函数被自动调用，用于需要手动管理资源的生命周期场景。
