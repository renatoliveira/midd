'''
Buids the report.
'''
import tempfile
import webbrowser

def generate(similar_images: dict):
    '''
    files are stored as filename => list of filenames
    '''
    file = tempfile.NamedTemporaryFile(
        mode='w',
        encoding='utf-8',
        delete=False,
        suffix='.html'
    )
    rows = []
    for image in similar_images.keys():
        similars = similar_images[image]
        if similars:
            row = '''
                <tr>
                    <td>
                        <p><img style="width: 50%;" src="file://{}"></p>
                        <p><code>{}</code></p>
                    </td>'''.format(image, image)
            row += '<td>'
            for sim in similars:
                row += '''
                <div>
                    <p><img style="width: 50%;" src="file://{}"></p>
                    <p><code>{}</code></p>
                </div>'''.format(sim, sim)
            row += '</td></tr>'
            rows.append(row)
    html = '<html><body><table>{}</table></body></html>'.format(''.join(rows))
    file.write(html)
    webbrowser.open('file://' + file.name)
