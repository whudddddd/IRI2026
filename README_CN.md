# IRI2026 Python 库

IRI2026 是国际参考电离层模型的 Python 接口，底层调用项目中包含的
Fortran 2026 模型代码。Python 接口返回 `xarray.Dataset`，使用方式参考
`iri2020` 项目的 build-on-first-use 结构。

## 安装

安装已经生成的 wheel：

```powershell
python -m pip install dist/iri2026-1.0.0-py3-none-any.whl
```

从源码安装：

```powershell
python -m pip install -e ".[tests]"
```

源码首次运行需要安装 CMake 和 Fortran 编译器，例如 gfortran。

## 基本使用

```python
import iri2026

iono = iri2026.IRI(
    "2026-09-28T12:00:00",
    (100, 1000, 10),
    35.0,
    120.0,
)

print(iono["ne"])
print(iono["Te"])
print(iono["TEC"])
```

参数顺序为：

```text
时间, [最低高度(km), 最高高度(km), 高度步长(km)], 纬度, 经度
```

## 命令行工具

安装后可以使用：

```text
iri2026-altitude 2026-09-28T12:00 35 120
iri2026-latitude 2026-09-28T12:00 120
iri2026-times 2026-09-28 2026-09-29 1 35 120
```

也可以直接运行模块：

```powershell
python -m iri2026.altitude 2026-09-28T12:00 35 120
```

## 开发和测试

```powershell
python -m pip install -e ".[tests,lint]"
python -m pytest
python -m pip wheel . --no-deps --wheel-dir dist
```

Fortran 驱动也可以直接使用 CMake 构建：

```powershell
cmake -S src/iri2026 -B src/iri2026/build -G "MinGW Makefiles"
cmake --build src/iri2026/build --parallel
```

## 目录结构

```text
src/iri2026/       Python 包和构建入口
src/iri2026/src/   Fortran 源码和 CMake 文件
src/iri2026/data/  IRI 系数、IGRF 和索引数据
tests/             Python 冒烟测试
examples/          IRI2020/IRI2026 对比程序
docs/              原始 IRI2026 文档
```

## 上传 GitHub

```powershell
git init
git add .
git commit -m "Prepare IRI2026 Python package"
git branch -M main
git remote add origin <GitHub仓库地址>
git push -u origin main
```

构建缓存、wheel、虚拟环境和本地编译文件已由 `.gitignore` 排除。
