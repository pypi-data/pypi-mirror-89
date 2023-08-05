import torch.nn as nn

def model2src(model, file='converted_model.py'):

    assert isinstance(model, nn.Module), 'model should be nn.Module instance.'

    s = [
"""
import torch
import torch.nn as nn
"""
    ]

    indent = 0
    stack = []

    is_defined = set()

    def parse_sequential(sequential, parent_name=None):
        block = ''
        # block += ' ' * indent * 4 + f'self.{name} = nn.ModuleList()\n'
        for name, module in sequential._modules.items():
            class_name = module.__class__.__name__

            if class_name in ['ModuleList', 'Sequential']:  # parse_sequential可能有.0
                if name.isdecimal():  # 名字是数字
                    pass
                var_name = 'fucky'
                block += ' ' * indent * 4 + f'{var_name} = nn.{class_name}()\n'
                block += ' ' * indent * 4 + f"{parent_name}.add_module('{name}', {var_name})\n"
                #     pass
                # else:  #
                #     block += ' ' * indent * 4 + f'{name} = nn.{class_name}()\n'

                block += parse_sequential(module, var_name) + '\n'
            else:
                if hasattr(nn, class_name):
                    block += ' ' * indent * 4 + f"{parent_name}.add_module('{name}', nn.{repr(module)})\n"
                else:
                    # ipdb.set_trace()
                    # if class_name == 'multi_scale':
                    #     print(s)
                    if class_name not in is_defined:
                        s.append(parse_model(module, class_name))
                        is_defined.add(class_name)
                    block += ' ' * indent * 4 + f"{parent_name}.add_module('{name}', {class_name}())\n"

        return block


    def parse_model(model, parent_name=None):
        block = \
        f"""
class {parent_name}(nn.Module):
    def __init__(self):
        super({parent_name}, self).__init__()
"""

        for name, module in model._modules.items():
            class_name = module.__class__.__name__

            if class_name in ['ModuleList', 'Sequential']:  # parse_model不可能出现self.0
                block += ' ' * indent * 4 + f'self.{name} = nn.{class_name}()\n'
                block += parse_sequential(module, f'self.{name}') + '\n'
            else:
                if hasattr(nn, class_name):
                    block += ' ' * indent * 4 + f"self.{name} = nn.{repr(module)}\n"
                else:
                    # ipdb.set_trace()
                    if class_name not in is_defined:
                        s.append(parse_model(module, class_name))
                        is_defined.add(class_name)
                    block += ' ' * indent * 4 + f"self.{name} = {class_name}()\n"

        block += \
"""
    def forward(self, x):
        return x
"""

        return block


    indent = 2
    p = parse_model(model, model.__class__.__name__)
    s += p

    simplified = {
        ', eps=1e-05, momentum=0.1, affine=True, track_running_stats=True': '',
        '(1, 1)': '1',
        '(2, 2)': '2',
        '(3, 3)': '3',
        '(4, 4)': '4',
        '(5, 5)': '5',
        ', mode=bilinear': ', mode="bilinear"',
    }

    s = ''.join(s)
    for i, j in simplified.items():
        s = s.replace(i, j)

    s += \
        f"""
if __name__ == '__main__':
    model = {model.__class__.__name__}()
    print(model)
"""
    
    with open(file, 'w') as f:
        f.write(s)
    print(f'Converted "{model.__class__.__name__}" source file is saved to "{file}".')

    # utils.p(list(model.state_dict().keys()))

