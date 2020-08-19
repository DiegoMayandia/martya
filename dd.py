from pywebcopy import save_webpage

kwargs = {'project_name': 'some-fancy-name'}

save_webpage(
    url='https://www.agatashoes.com/collections/todo-zapatos/products/zapatillas-berta-negro-zebra-cuero-legitimo',
    project_folder='downloads',
    **kwargs
)