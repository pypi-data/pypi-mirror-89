#!/usr/bin/env python3
'''
Python3 multipart upload function for presigned URLs with multiprocessing.
'''

# Insist on Python3 or later.
import sys
try:
    assert sys.version_info[0] >= 3
except Exception as e:
    print('Python version error. You need to use Python3 or later.')

# Make sure all necessary modules are available.
try:
    import ast
    import json
    import os
    import random
    import requests
    import string
    import time
    from multiprocessing import Pool
    from tqdm import tqdm
except Exception as e:
    print('Module import error. You may need to install extra Python3 module(s).')
    print(str(e))

# Systems initializations:
namels = []
manifestls = []
sentinel = 555

# Check read access.
def checkread(fileloc):
    try:
        os.access(fileloc, os.R_OK)
        return {'status': 200, 'response': 'OK'}
    except Exception as e:
        print('No read access to source document: {} \n{}'.format(fileloc, str(e)))
        return {'status': sentinel, 'response': str(e)}

# Check write access.
def checkwrite(tmp):
    try:
        os.access(tmp, os.W_OK)
        return {'status': 200, 'response': 'OK'}
    except Exception as e:
        print('No write access to temporary directory: {} \n{}'.format(tmp, str(e)))
        return {'status': sentinel, 'response': str(e)}

# Create unique filenames.
def mknewfilename(filename):
    try:
        newname = filename.replace('.' + filename.split('.')[-1], '') + '_' + str(int(time.time())) + '_' + ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=5))
        newfilename = newname + '.' + filename.split('.')[-1] + '.'
        return {'status': 200, 'response': newfilename}
    except Exception as e:
        return {'status': sentinel, 'response': str(e)}

# Get Upload ID.
def getid(overwrite, requrl, code, filename, path, domain):
    try:
        with tqdm(desc = 'Getting Upload ID for {}/{}/{}...'.format(domain, path, filename), leave = False, bar_format = '{desc}'):
            if overwrite == 'YES':
                response = requests.post(requrl + '?action=create&code=' + code, data = '{"filename": "' + path + '/' + filename + '", "overwrite": "YES"}')
            else:
                response = requests.post(requrl + '?action=create&code=' + code, data = '{"filename": "' + path + '/' + filename + '"}')
        assert response
        return {'status': 200, 'response': response.text}
    except Exception as e:
        return {'status': sentinel, 'response': response.text}

# Get pre-signed URL for each chunk.
def presignit(requrl, code, chunkedfile):
    try:
        with tqdm(desc = 'Getting pre-signed URL for part: {}...'.format(chunkedfile), leave = False, bar_format = '{desc}'):
            response = requests.get(requrl + '?action=geturl&code=' + code + '&filename=tmp/' + chunkedfile)
        answer = ast.literal_eval(response.text)
        assert response
        return {'status': 200, 'response': answer}
    except Exception as e:
        return {'status': sentinel, 'response': response.text}

# Upload chunks to temporary location on storage.
def uploadit(requrl, code, chunkedfile, files):
    try:
        with tqdm(desc = 'Uploading {}...'.format(chunkedfile), leave = False, bar_format = '{desc}'):
            response = requests.post(presignit(requrl, code, chunkedfile)['response']['url'], data = presignit(requrl, code, chunkedfile)['response']['fields'], files = files)
        assert response
        return {'status': 200, 'response': response}
    except Exception as e:
        return {'status': sentinel, 'response': response.text}

# Add chunks to multipart.
def addit(requrl, code, filename, path, uploadid, chunkedfile, filenum):
    try:
        response = requests.post(requrl + '?action=add&code=' + code, data = '{"filename": "' + path + '/' + filename + '", "uploadid": "' + uploadid + '", "partname": "tmp/' + chunkedfile + '", "partnumber": "' + filenum + '"}')
        assert response
        return {'status': 200, 'response': 'OK'}
    except Exception as e:
        return {'status': sentinel, 'response': response.text}

# Purge document from storage.
def purgeit(requrl, domain, code, filename, path):
    try:
        with tqdm(desc = 'Purging {}/{}/{} from storage...'.format(domain, path, filename), leave = False, bar_format = '{desc}'):
            manifestpurge = [{'Key': path + '/' + filename}]
            response = requests.post(requrl + '?action=purge&code=' + code, data = '{"filename": "' + path + '/' + filename+'", "objects": "' + str(manifestpurge) + '"}')
        assert response
        return {'status': 200, 'response': 'OK'}
    except Exception as e:
        return {'status': sentinel, 'response': response.text}

# Purge document from CDN. Only needed during overwrite and purge. New files don't need CDN cache purging.
def cdnpurgeit(cdnurl, domain, code, filename, path):
    try:
        with tqdm(desc = 'Purging {}/{}/{} from CDN cache...'.format(domain, path, filename), leave = False, bar_format = '{desc}'):
            response = requests.post(cdnurl + '?code=' + code + '&urls=' + domain + '/' + path + '/' + filename)
        assert response
        return {'status': 200, 'response': 'OK'}
    except Exception as e:
        return {'status': sentinel, 'response': response.text}

# Abort multipart upload if any of the parts fails.
def abortit(requrl, code, filename, path, uploadid, fileloc):
    try:
        with tqdm(desc= 'Aborting upload for {}...'.format(fileloc), leave = False, bar_format='{desc}'):
            response = requests.post(requrl + '?action=abort&code=' + code, data = '{"filename": "' + path + '/' + filename+'", "uploadid": "' + uploadid + '"}')
        assert response
        return {'status': 200, 'response': 'OK'}
    except Exception as e:
        return {'status': sentinel, 'response': response.text}

# Delete temporary files from storage.
def deleteit(requrl, code, filename, path, manifestdel):
    try:
        with tqdm(desc= 'Deleting temporary files...', leave = False, bar_format='{desc}'):
            response = requests.post(requrl + '?action=delete&code=' + code, data = '{"filename": "' + path + '/' + filename+'", "objects": "' + str(manifestdel) + '"}')
        assert response
        return {'status': 200, 'response': 'OK'}
    except Exception as e:
        return {'status': sentinel, 'response': response.text}

# Complete multipart upload if everything is good.
def completeit(requrl, code, filename, path, uploadid, manifest):
    try:
        with tqdm(desc= 'Recombining parts...', leave = False, bar_format='{desc}'):
            response = requests.post(requrl + '?action=complete&code=' + code, data = '{"filename": "' + path + '/' + filename + '", "uploadid": "' + uploadid + '", "parts": "' + str(manifest) + '"}')
        assert response
        return {'status': 200, 'response': 'OK'}
    except Exception as e:
        return {'status': sentinel, 'response': response.text}

# Work on each chunk.
def chunkit(chunkeddict):
    uploadid = list(chunkeddict.keys())[-1]
    chunkedfile = chunkeddict['chunkedfile']
    uploadid = chunkeddict['uploadid']
    requrl = chunkeddict['requrl']
    code = chunkeddict['code']
    filename = chunkeddict['filename']
    path = chunkeddict['path']

    # Get file numbering from the new filenames.
    filenum = chunkedfile.split('.')[-1]

    ### All upload processes go here. ###
    try:

        # Attempt upload up to 3 times for each chunk. Return 204 if chunk is good, or anoother status code depending on the failure.
        uploadcount = 1
        chunkstatus = 1
        while uploadcount < 4 and chunkstatus != 204:
            with open(chunkedfile, 'rb') as m:
                files = {'file': (chunkedfile, m)}
                preresponse = uploadit(requrl, code, chunkedfile, files)
                try:
                    assert preresponse['status'] == 200
                    response = preresponse['response']
                    etag = response.headers['ETag'].strip('"')
                    chunkstatus = response.status_code
                except:
                    chunkstatus = sentinel

            # Print chunk upload status, briefly.
            if chunkstatus != 204:
                with tqdm(desc = '{} Failed'.format(chunkedfile), leave = False, bar_format = '{desc}'):
                    pass
            else:
                with tqdm(desc = '{} OK'.format(chunkedfile), leave = False, bar_format = '{desc}'):
                    pass
            uploadcount += 1
        
        # Stop processing if chunk fails continuously, otherwise keep working.
        if chunkstatus != 204:
            print('Part {}: Failed'.format(chunkedfile))
            print('Upload attempt for {} failed after 3 tries.'.format(chunkedfile))

            # Create upload manifest.
            try:
                manifestcontent = manifestcontent = {'status': 'failed'}
                # Remove current chunk from local temporary storage.
                os.remove(chunkedfile)
                return manifestcontent
            except:
                # Abort multipart upload upon failure to clean storage from rogue Upload ID.
                preresponse = abortit(requrl, code, filename, path, uploadid, fileloc)
                try:
                    assert preresponse['status'] == 200
                    os.remove(chunkedfile)
                except Exception as e:
                    print(preresponse['response'])
                    os.remove(chunkedfile)
                    sys.exit(1)

        else:
            print('Part {}: OK'.format(chunkedfile))

            # Add chunk to document manifest.
            preresponse = addit(requrl, code, filename, path, uploadid, chunkedfile, filenum)
            try:
                assert preresponse['status'] == 200
            except Exception as e:
                print('Part {}: Failed'.format(chunkedfile))
                print(preresponse['response'])

                # Abort multipart upload upon failure to clean storage from rogue Upload ID.
                preresponse = abortit(requrl, code, filename, path, uploadid, fileloc)
                try:
                    assert preresponse['status'] == 200
                    os.remove(chunkedfile)
                except Exception as e:
                    print(preresponse['response'])
                    os.remove(chunkedfile)
                    sys.exit(1)

            # Create upload manifest.
            try:
                manifestcontent = {'ETag': etag, 'PartNumber': int(filenum), 'Key': 'tmp/' + chunkedfile}
                # Remove current chunk from local temporary storage.
                os.remove(chunkedfile)
                return manifestcontent
            except:
                # Abort multipart upload upon failure to clean storage from rogue Upload ID.
                preresponse = abortit(requrl, code, filename, path, uploadid, fileloc)
                try:
                    assert preresponse['status'] == 200
                    os.remove(chunkedfile)
                except Exception as e:
                    print(preresponse['response'])
                    os.remove(chunkedfile)
                    sys.exit(1)
            
    # Abort and delete multiipart upload if failed.
    except Exception as e:
        print(str(e))
        # Signal the loop that a chunk has failed.
        manifestcontent = {'status': 'failed'}
        # Remove current chunk from local temporary storage.
        os.remove(chunkedfile)
        return manifestcontent

# Multiprocessing.
def poolit(parts, namelist):
    with Pool(parts) as p:
        results = p.map(chunkit, namelist)
        if {'status': 'failed'} in results:
            p.terminate()
    return results

def multipart(code, fileloc, path, parts = 5, partsize = 100, tmp = '/tmp', overwrite = 'NO', purge = 'NO', domain = 'https://storage.url', requrl = 'https://backend.url', cdnurl = 'https://cdn.url'):

    # Parameter processing.
    fileloc = fileloc.strip().rstrip('/')
    filedir = os.path.dirname(fileloc) if os.path.dirname(fileloc) != '' else '.'
    filename = os.path.basename(fileloc)
    path = path.strip().strip('/')
    tmp = tmp.rstrip('/')
    partsize = partsize * 1048576
    domain = domain.rstrip('/')
    requrl = requrl.rstrip('/')
    cdnurl = cdnurl.rstrip('/')

    # Check if locations have correct permissions.
    checkread(fileloc)
    checkwrite(tmp)

    # Purge object from storage.
    if purge == 'YES':

        # Purge document.
        preresponse = purgeit(requrl, domain, code, filename, path)
        try:
            assert preresponse['status'] == 200
        except Exception as e:
            print(preresponse['response'])
            return {'status': 500, 'response': preresponse['response']}
            sys.exit(1)
        
        # Purge document cache from CDN if storage purge was successful.
        preresponse = cdnpurgeit(cdnurl, domain, code, filename, path)
        try:
            assert preresponse['status'] == 200
            print('Document purged from storage and CDN.')
            return {'status': 200, 'response': 'Document purged from storage and CDN.'}
            sys.exit(0)
        except Exception as e:
            print(preresponse['response'])
            return {'status': 500, 'response': preresponse['response']}
            sys.exit(1)

    # Engage!
    try:

        # Open file for reading.
        with open(filedir + '/' + filename, 'rb') as f:

            # Get Upload ID from storage.
            preresponse = getid(overwrite, requrl, code, filename, path, domain)
            try:
                assert preresponse['status'] == 200
                uploadid = preresponse['response']
            except Exception as e:
                print(preresponse['response'])
                return {'status': 500, 'response': preresponse['response']}
                sys.exit(1)
            
            # Create temporary filename for chunking.
            preresponse = mknewfilename(filename)
            try:
                assert preresponse['status'] == 200
                newfilename = preresponse['response']
            except Exception as e:
                print(preresponse['response'])

                # Abort multipart upload upon failure to clean storage from rogue Upload ID.
                preresponse = abortit(requrl, code, filename, path, uploadid, fileloc)
                try:
                    assert preresponse['status'] == 200
                except Exception as e:
                    print(preresponse['response'])
                    return {'status': 500, 'response': preresponse['response']}
                    sys.exit(1)
            
            # Work through the file until all chunks are uploaded.
            chunknum = 1
            while True:
                data = f.read(partsize)
                if not data:
                    break
                with open(tmp + '/' + newfilename + str(chunknum), 'wb') as fchunk:
                    fchunk.write(data)
                namels.append({'requrl': requrl, 'code': code, 'filename': filename, 'path': path, 'uploadid': uploadid, 'chunkedfile': tmp + '/' + newfilename + str(chunknum)})
                chunknum += 1
                if chunknum > 1 and chunknum % parts == 1:
                    results = poolit(parts, namels)
                    manifestls.extend(results)
                    if {'status': 'failed'} in manifestls:
                        raise Exception('Failed to complete upload.')
                    namels.clear()
            results = poolit(parts, namels)
            manifestls.extend(results)
            if {'status': 'failed'} in manifestls:
                raise Exception('Failed to complete upload.')
            namels.clear()
        
        # Finalize if everything is good.
        try:

            # Create manifest lists for recombination and teporary file deletion.
            try:
                manifest = [{'ETag': i['ETag'], 'PartNumber': i['PartNumber']} for i in manifestls]
                manifestdel = [{'Key': i['Key']} for i in manifestls]
            
            except Exception as e:
                print('Upload failed, temporary files could not be deleted. \n{}'.format(str(e)))

                # Abort multipart upload upon failure to clean storage from rogue Upload ID.
                preresponse = abortit(requrl, code, filename, path, uploadid, fileloc)
                try:
                    assert preresponse['status'] == 200
                except Exception as e:
                    print(preresponse['response'])
                    return {'status': 500, 'response': preresponse['response']}
                    sys.exit(1)

            # Complete multipart upload.
            preresponse = completeit(requrl, code, filename, path, uploadid, manifest)
            try:
                assert preresponse['status'] == 200
            except Exception as e:
                print(preresponse['response'])

                # Abort multipart upload upon failure to clean storage from rogue Upload ID.
                preresponse = abortit(requrl, code, filename, path, uploadid, fileloc)
                try:
                    assert preresponse['status'] == 200
                except Exception as e:
                    print(preresponse['response'])
                    return {'status': 500, 'response': preresponse['response']}
                    sys.exit(1)

            # Delete temporary files.
            preresponse = deleteit(requrl, code, filename, path, manifestdel)
            try:
                assert preresponse['status'] == 200
                print('Upload complete: {}/{}/{}'.format(domain, path, filename))
            except Exception as e:
                print('Upload complete: {}/{}/{}. Temporary files could not be deleted.'.format(domain, path, filename))
                print(preresponse['response'])

            # Purge the document from CDN if overwriting.
            if overwrite == 'YES':
                preresponse = cdnpurgeit(cdnurl, domain, code, filename, path)
                try:
                    assert preresponse['status'] == 200
                    print('Document purged from CDN.')
                except Exception as e:
                    print(preresponse['response'])
                    return {'status': 500, 'response': preresponse['response']}
                    sys.exit(1)

            return {'status': 200, 'response': 'Upload complete.'}

        except Exception as e:
            print(str(e))
            return {'status': 500, 'response': 'Upload failed.'}

    # Abort if something's wrong.
    except Exception as e:

        # If failed on the first chunk.
        if manifestls == [{'status': 'failed'}]:

            # Abort multipart upload upon failure to clean storage from rogue Upload ID.
            preresponse = abortit(requrl, code, filename, path, uploadid, fileloc)
            try:
                assert preresponse['status'] == 200
            except Exception as e:
                print(preresponse['response'])
                return {'status': 500, 'response': preresponse['response']}
                sys.exit(1)

        # If failed on a subsequent chunk.
        elif {'status': 'failed'} in manifestls:
            manifestdel = [{'Key': i['Key']} for i in manifestls]

            # Abort multipart upload upon failure to clean storage from rogue Upload ID.
            preresponse = abortit(requrl, code, filename, path, uploadid, fileloc)
            try:
                assert preresponse['status'] == 200
            except Exception as e:
                print(preresponse['response'])

            # Delete temporary files from storage.
            preresponse = deleteit(requrl, code, filename, path, manifestdel)
            try:
                assert preresponse['status'] == 200
            except Exception as e:
                print(preresponse['response'])
                return {'status': 500, 'response': preresponse['response']}
                sys.exit(1)

        else:
            pass

        return {'status': 500, 'response': 'Upload failed.'}
        print(str(e))
