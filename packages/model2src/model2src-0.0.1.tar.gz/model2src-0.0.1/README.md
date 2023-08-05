# Model2src

Convert pytorch model to source file.

### Installation

**For pip**  

```bash
pip install model2src
```


### Usage

```python
from torchvision.models import vgg16
from model2src import model2src
model = vgg16()
model2src(model)
```

Of course, you can also convert yourself's models as well.