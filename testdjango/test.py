def clean(self):
    cleaned_data = self.cleaned_data
    url = cleaned_data.get('url')
    # 如果 url 字段不为空，而且不以“http://”开头
    # 在前面加上“http://”
    if url and not url.startswith('http://'):
        url = 'http://' + url
    cleaned_data['url'] = url
    return cleaned_data