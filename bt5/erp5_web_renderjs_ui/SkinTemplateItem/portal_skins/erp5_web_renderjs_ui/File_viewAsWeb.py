if REQUEST is None:
  REQUEST = context.REQUEST
if response is None:
  response = REQUEST.RESPONSE

file = context
file_content = file.getData()

# The vanilla HTML is wanted
response.setBase(None)

if REQUEST.getHeader('If-Modified-Since', '') == file.getModificationDate().rfc822():
  response.setStatus(304)
  return ""

#file_content_type = file.getContentType()
#if file_content_type is None:
#  file_content_type = 'application/octet-stream'

response.setHeader('Content-Type', (file.getContentType() or 'application/octet-stream'))

return file_content
