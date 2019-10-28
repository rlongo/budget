from collections import namedtuple

class Generator:
    '''
    Generates HTML based on the local header and footer html files.
    HTML styled via bulma.io
    '''

    Content = namedtuple('Content', 'type content_subheading val msg')
    _DATA_IMG = 'img'
    _DATA_TABLE = 'table'
    _DATA_TEXT = 'text'
    
    def __init__(self):
        self._sections = []

    def _get_section_list(self, section):
        for s, l in self._sections:
            if s == section:
                return l
        new_entry = (section, [])
        self._sections.append(new_entry)
        return new_entry[1]

    def _append_section_list(self, section, content):
        self._get_section_list(section).append(content)

    def add_section_image(self, section, content_subheading, path, msg=None):
        payload = Generator.Content(Generator._DATA_IMG, content_subheading, path, msg)
        self._append_section_list(section, payload)
    
    def add_section_dataframe(self, section, content_subheading, df, msg=None):
        v = df.to_html().replace('dataframe', 'table')
        payload = Generator.Content(Generator._DATA_TABLE, content_subheading, v, msg)
        self._append_section_list(section, payload)
   
    def add_section_text(self, section, content_subheading, text):
        payload = Generator.Content(Generator._DATA_TEXT, content_subheading, text, None)
        self._append_section_list(section, payload)

    def generate(self, path):
        with open(path, 'w') as o:
            
            # Add the header
            with open('header.html') as h:
                o.writelines(h.readlines())
           
            # Add individual sections
            for s, c in self._sections:
                self._write_section(o, s, c)

            # Add the footer
            with open('footer.html') as f:
                o.writelines(f.readlines())

    def _write_section(self, fd, section, content):
        handler = dict()
        handler[Generator._DATA_IMG] = self._write_content_img
        handler[Generator._DATA_TABLE] = self._write_content_table
        handler[Generator._DATA_TEXT] = self._write_content_text

        fd.write('<section class="section">\n <div class="container">\n')
        fd.write('<h1 class="title">%s</h1>\n' % section)
        for c in content:
            if c.content_subheading:
                fd.write('<h2 class="subtitle">%s</h2>\n' % c.content_subheading)
            if c.msg:
                fd.write('<p>%s</p>\n' % c.msg)
            handler[c.type](fd, c.val)
        fd.write('</div>\n</section>\n')

    def _write_content_img(self, fd, val):
        fd.write('<figure class="image"><img src="%s"></figure>\n' % val)

    def _write_content_table(self, fd, table):
        fd.write(table + '\n')

    def _write_content_text(self, fd, val):
        fd.write('<p>%s</p>\n' % val)


if __name__=='__main__':
    g = Generator()
    g.add_section_text('Section A', 'Subheading a', 'Here is some text')
    g.add_section_text('Section A', None, 'Here is some more text')
    g.add_section_text('Section B', 'Subheading', 'Here is some more text')
    g.add_section_image('Section B', None, 'https://bulma.io/images/placeholders/128x128.png')
    g.generate('output.html')
