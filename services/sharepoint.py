

def get_files(file_url, ctx):
    try:        
        list_source = ctx.web.get_folder_by_server_relative_url(file_url)
        files = list_source.files
        ctx.load(files)
        ctx.execute_query()

        return files

    except Exception as e:
        print(e)



def post_files(file_url,filepath, ctx):
    try:

        list_source = ctx.web.get_folder_by_server_relative_url(file_url)

        with open(filepath, 'r') as content_file:
            file_content = content_file.read()
            
            list_source.upload_file(filepath, file_content).execute_query()

    except Exception as e:
        print(e)
