在 **Python 项目中，从文件夹 A 的类导入文件夹 B 的类**，常见有 3 种方式。关键取决于你的 **项目目录结构**。我用一个标准示例说明。

---

# 一、推荐方式：使用包导入（最规范）

假设项目结构：

```
project/
│
├── folderA/
│   ├── __init__.py
│   └── a.py
│
├── folderB/
│   ├── __init__.py
│   └── DateUtils.py
│
└── main.py
```

DateUtils.py

```python
class DateUtils:
    @staticmethod
    def now():
        return "2026-03-07"
```

---

## 在 folderA/a.py 导入

```python
from folderB.DateUtils import DateUtils

print(DateUtils.now())
```

运行时：

```
python main.py
```

或者

```
python -m folderA.a
```

---

# 二、相对路径导入（包内部推荐）

如果 **folderA 和 folderB 同级**，可以：

```
project
 ├ folderA
 │   └ a.py
 └ folderB
     └ DateUtils.py
```

在 `folderA/a.py`

```python
from ..folderB.DateUtils import DateUtils
```

⚠️ 注意：

必须通过 **模块方式运行**

```
python -m folderA.a
```

不能直接

```
python a.py
```

否则会报错：

```
ImportError: attempted relative import with no known parent package
```

---

# 三、修改 sys.path（简单粗暴但不推荐）

如果你只是临时脚本，可以这样：

```python
import sys
import os

sys.path.append(os.path.abspath('../folderB'))

from DateUtils import DateUtils
```

但这种方式：

* 不优雅
* 不利于维护
* 不适合正式项目

---

# 四、最标准 Python 项目结构（推荐）

如果你是 **正式项目**，建议这样：

```
my_project/
│
├── app/
│   ├── __init__.py
│   ├── folderA/
│   │    └ a.py
│   └── folderB/
│        └ DateUtils.py
│
└── main.py
```

导入：

```python
from app.folderB.DateUtils import DateUtils
```

---

# 五、很多人遇到的错误

### 错误1

```
ModuleNotFoundError: No module named 'DateUtils'
```

原因：

* Python 找不到模块路径

解决：

* 使用 **完整包路径**

```
from folderB.DateUtils import DateUtils
```

---

### 错误2

缺少 `__init__.py`

Python 需要这个文件识别为 **package**

```
folderA/__init__.py
folderB/__init__.py
```

可以是空文件。

---

# 六、你写的这句代码的问题

你写的是：

```python
from DateUtils import DateUtils
```

只有在 **同一个目录** 才可以这样。

如果在不同目录，应该：

```
from folderB.DateUtils import DateUtils
```

---

💡 如果你愿意，可以把你的 **Python 项目目录结构发出来，例如：**

```
project
 ├ A
 │  └ xxx.py
 └ B
    └ DateUtils.py
```

我可以帮你写 **最正确的导入方式**（避免以后 import 出问题）。

---
在 Python 中从文件夹 A 导入文件夹 B 中的类，核心是**让文件夹成为可导入的模块（添加 `__init__.py`）**，并确保 Python 能找到这些文件夹的路径。我会分场景详细讲解，从最简单的同级文件夹到跨目录的情况。

### 先明确目录结构（以你的需求为例）
假设你的项目结构如下（先定义通用结构，方便理解）：
```
你的项目根目录/
├── 文件夹A/          # 存放 DateUtils.py 的文件夹
│   ├── __init__.py   # 必须有！让文件夹A成为Python模块
│   └── DateUtils.py  # 里面有 DateUtils 类
└── 文件夹B/          # 你要导入到这里的目标文件夹
    ├── __init__.py   # 必须有！让文件夹B成为Python模块
    └── 你的脚本.py   # 你要写 from DateUtils import DateUtils 的文件
```

### 场景1：文件夹A 和 文件夹B 是**同级目录**（最常见）
即两个文件夹在同一个项目根目录下，这是最简单的情况。

#### 步骤 1：给两个文件夹添加 `__init__.py`
- 在 `文件夹A/` 和 `文件夹B/` 下各创建一个空文件，命名为 `__init__.py`（注意前后各两个下划线）。
  - 这个文件的作用：告诉 Python “这个文件夹不是普通文件夹，是可以导入的模块”。

#### 步骤 2：在文件夹B的脚本中导入
```python
# 文件夹B/你的脚本.py
# 方式1：直接从同级模块导入（推荐）
from 文件夹A.DateUtils import DateUtils

# 方式2：先导入模块，再取类（适合需要多次使用该模块的场景）
import 文件夹A.DateUtils as du
from 文件夹A import DateUtils  # 也可以先导入模块，再用 DateUtils.DateUtils 调用类

# 测试使用
if __name__ == "__main__":
    date_obj = DateUtils()  # 实例化导入的类
    print(date_obj)
```

### 场景2：文件夹A 和 文件夹B 不是同级（跨目录）
如果目录结构是嵌套的（比如 A 在根目录，B 在根目录的子文件夹里，或反过来），需要调整导入路径，或把项目根目录加入 Python 搜索路径。

#### 示例目录（A 是根目录，B 在子目录）：
```
你的项目根目录/
├── 文件夹A/          # 根目录下的A
│   ├── __init__.py
│   └── DateUtils.py
└── src/              # 子目录
    └── 文件夹B/      # B 在 src 下
        ├── __init__.py
        └── 你的脚本.py
```

#### 解决方案：添加项目根目录到 Python 路径
在 `文件夹B/你的脚本.py` 开头添加以下代码，手动把项目根目录加入 Python 的搜索路径，再导入：
```python
# 文件夹B/你的脚本.py
import sys
import os

# 获取项目根目录的绝对路径（根据你的目录结构调整）
# __file__ 是当前脚本的路径，os.path.dirname 逐级向上找父目录
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
# 把根目录加入Python搜索路径
sys.path.append(PROJECT_ROOT)

# 现在就可以像同级目录一样导入了
from 文件夹A.DateUtils import DateUtils

# 测试使用
date_obj = DateUtils()
```

### 场景3：文件夹A 不在项目根目录（完全独立）
如果文件夹A 是一个完全独立的目录（比如在桌面，而你的项目在文档里），有两种方式：
#### 方式1：临时添加路径（推荐，不修改系统环境）
```python
# 文件夹B/你的脚本.py
import sys
# 直接添加文件夹A的绝对路径
sys.path.append("文件夹A的绝对路径")  # 比如："C:/项目/文件夹A" 或 "/Users/xxx/桌面/文件夹A"

# 然后导入
from DateUtils import DateUtils  # 因为A的路径已加入，直接导入模块
```

#### 方式2：把文件夹A 添加到系统环境变量（永久生效）
- Windows：在系统环境变量 `PYTHONPATH` 中添加文件夹A的绝对路径。
- Mac/Linux：在 `.bashrc` 或 `.zshrc` 中添加 `export PYTHONPATH=$PYTHONPATH:/文件夹A的绝对路径`，然后执行 `source ~/.bashrc` 生效。
- 优点：不用每次写 `sys.path.append`；缺点：只对当前系统生效。

### 关键补充：`__init__.py` 的进阶用法（可选）
如果想简化导入（比如不想写 `from 文件夹A.DateUtils import DateUtils`，而是 `from 文件夹A import DateUtils`），可以在 `文件夹A/__init__.py` 中添加：
```python
# 文件夹A/__init__.py
from .DateUtils import DateUtils  # . 表示当前模块（文件夹A）
```
这样在文件夹B中就可以简化导入：
```python
from 文件夹A import DateUtils  # 更简洁
```

### 常见报错及解决
1. `ModuleNotFoundError: No module named '文件夹A'`：
   - 原因：Python 找不到文件夹A的路径，或文件夹A没有 `__init__.py`。
   - 解决：添加 `__init__.py`，或用 `sys.path.append` 把项目根目录加入路径。
2. `ImportError: cannot import name 'DateUtils' from '文件夹A.DateUtils'`：
   - 原因：DateUtils.py 中没有定义 DateUtils 类，或类名拼写错误。
   - 解决：检查 DateUtils.py 中的类名是否正确（比如是不是 `class DateUtils:`）。

---

### 总结
1. **核心前提**：被导入的文件夹（A）必须包含 `__init__.py`（空文件即可），使其成为 Python 模块。
2. **同级目录导入**：直接 `from 文件夹A.模块名 import 类名`。
3. **跨目录导入**：先通过 `sys.path.append(项目根目录)` 让 Python 找到路径，再按同级方式导入。
4. **简化导入**：可在文件夹A的 `__init__.py` 中提前导出类，让导入语句更简洁。