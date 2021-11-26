import getopt
import os
import sys
import zipfile
import mosspy   # https://github.com/soachishti/moss.py
import shutil

def createOutputFolder(folderName):
    if not os.path.exists(folderName):
        os.makedirs(folderName)

def unzipSubmissions(inputFile, outputFolder):
    print('Extracting from: ' + inputFile)
    createOutputFolder(outputFolder)
    with zipfile.ZipFile(inputFile, 'r') as submissions:
        for filename in submissions.namelist():
            # extract the student name and use that as the folder name to store the files
            studentName = filename[0:filename.find('_')]
            createOutputFolder(os.path.join(outputFolder, studentName))
            # If the file itself is a .zip file, pop it open and extract those files
            fileParts = os.path.splitext(filename)
            if fileParts[1] == '.zip':
                submissions.extract(filename, os.path.join(outputFolder, studentName))
                zipFilename = os.path.join(outputFolder, studentName, filename)
                #print('zip filename: ' + zipFilename)
                with zipfile.ZipFile(zipFilename, 'r') as internalZip:
                    for internalFile in internalZip.namelist():
                        #print('internal file of zip: '+internalFile)
                        internalZip.extract(internalFile, os.path.join(outputFolder, studentName))
                os.remove(zipFilename)
            else:
                # Extract the file(s) for this student into the student folder
                submissions.extract(filename, os.path.join(outputFolder, studentName))

def submitSubmissions(outputFolder, userid, language):
    m = mosspy.Moss(userid, language)
    print('Collecting files to submit')
    m.setDirectoryMode(1)
    for name in os.listdir(outputFolder):
        path = os.path.join(outputFolder, name)
        if os.path.isdir(path):
            for filename in os.listdir(path):
                if os.path.isfile(os.path.join(path, filename)):
                    print('adding file: ', os.path.join(path, filename))
                    m.addFile(os.path.join(path, filename))
    print('Sending files to MOSS...')
    try:
        url = m.send()
        print('Report URL: ' + url)
        m.saveWebPage(url, "report.html")
        # mosspy.download_report(url, "assignment1/report/", connections = 8)
    except:
        e = sys.exc_info()[0]
        print('Exception: ', e)

def extract_all_source_files(outputFolder, file_ext='.java'):
    for name in os.listdir(outputFolder):
        path = os.path.join(outputFolder, name)
        if os.path.isdir(path):
            extract_source(path, path, file_ext)
            for f in os.listdir(path):
                p = os.path.join(path, f)
                if os.path.isdir(p):
                    try:
                        shutil.rmtree(p)
                    except:
                        print("Remove directory exceptions occured {}".format(p))
                else:
                    if os.path.splitext(f)[1] != file_ext:
                        try:
                            os.remove(p)                      # remove files
                        except:
                            print("Remove file exceptions occured {}".format(p))
        else:
            try:
                os.remove(path)   #remove desktop.ini file
            except:
                print("Remove file exceptions occured {}".format(path))

def extract_source(cur_path, root_folder, file_ext):
    for name in os.listdir(cur_path):
        path = os.path.join(cur_path, name)
        if os.path.isdir(path):
            extract_source(path, root_folder, file_ext)
        else:
            if os.path.splitext(name)[1]==file_ext:
                try:
                    shutil.copy(path, root_folder)
                except shutil.SameFileError:
                    print("Source and destination represents the same file: {}".format(path))
                except PermissionError:
                    print("Permission denied: {}".format(path))
                except:
                    print("Error occurred while copying file: {}".format(path))


def main(argv):
    try:
        inputFiles = []
        outputFolder = ''
        userid = ''
        language = ''
        file_ext = ''
        opts, args = getopt.getopt(argv, '',['infile=', 'outfolder=', 'userid=', 'language=', 'file_ext='])
    except getopt.GetoptError as ex:
        print('exception: ', ex.msg)
        print('checker.py --infile <inputfile> --outfolder <outputfolder> --userid <userid> --language <language>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '--help':
            print('checker.py --infile <inputfile> --outfolder <outputfolder> --userid <userid> --language <language>')
        elif opt == '--infile':
            inputFiles.append(arg)
        elif opt == '--outfolder':
            outputFolder = arg
        elif opt == '--userid':
            userid = arg
        elif opt == '--language':
            language = arg
        elif opt == '--file_ext':
            file_ext = '.'+arg
    for inputFile in inputFiles:
        unzipSubmissions(inputFile, outputFolder)
    extract_all_source_files(outputFolder)
    submitSubmissions(outputFolder, userid, language)

main(sys.argv[1:])
