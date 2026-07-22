def format_output(func):
    def wrapper(self):
        result = func(self)
        line = "----------------------------------------"
        return line + "\n" + result + "\n" + line
    return wrapper

class ReportGenerator:

    templates = {
        "plain": "{title}\n{content}",
        "boxed": "[{title}]\n{content}"
    }
    def __init__(self, title, content, template="plain"):
        self.title = title
        self.content = content
        self.template = template
    @classmethod
    def add_template(cls, name, template_text):
        cls.templates[name] = template_text
    @format_output
    def generate(self):
        chosen_template = self.templates[self.template]
        report_text = chosen_template.format(title=self.title, content=self.content)
        return report_text
    
    def __str__(self):
        return "Title: " + self.title + "\nTemplate: " + self.template + "\nContent: " + self.content

if __name__ == "__main__":

    ReportGenerator.add_template("banner", "*** {title} ***\n{content}")

    my_report = ReportGenerator("Sales Report", "Sales went up by 7% this month.", "banner")
    print(my_report)
    print()
    print(my_report.generate())