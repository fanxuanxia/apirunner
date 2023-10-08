from string import Template

class MyTemplate(Template):
    delimiter = "!"  # 需要用到前面步骤中的数据时，格式：！变量名，!作为占位符的标志