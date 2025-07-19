#---------------------------------------------------CHECK-INFO--------------------------------------------------------#
import sys
import os
import get_set_Data as app


#to check if all packages has been installed
def is_packages_installed():
    #packages
    packages=app.get_packages()

    if packages[0]:#if no problem during importation
       for package in packages[1]:
           try:
               __import__(package['name'])
           except ImportError:
               return [False,f"Package unistalled {package["name"]} command {package["command"]}"]#packages unistalled
    else:
        return packages    
    
    return [True,"Packages installed successfuly"] #if everything good

#to check if tensorflow and python is adapted
def is_version_adapted():
    #versions
    versions=app.get_version_adapted()

    if versions[0]: #if no problem during importation
        #to check python
        python_version=versions[1][0]["version"]
        actual_str=((sys.version).split()[0]).split(".")[:2]
        actual_version=[int(actual_str[0]),int(actual_str[1])]
        if actual_version<python_version[0] or actual_version>python_version[1]:
            return[False,f"your python version must be between or equal to {python_version[0]} or {python_version[1]} and your version is {actual_version}"]
       
        #to check tensorflow
        tensorflow_version=versions[1][1]["version"]
        actual_str=((__import__("tensorflow")).__version__).split(".")[:2]
        actual_version=[int(actual_str[0]),int(actual_str[1])]
        if actual_version<tensorflow_version[0] or actual_version>tensorflow_version[1]:
            return[False,f"your tensorflow version must be between or equal to {tensorflow_version[0]} or {tensorflow_version[0]} and your version is {actual_version}"]
        
        
        return [True,"Version adapted"] #everything is good

    else:
        return versions
    
#to check if all files are there and not changed
def is_files_exists():
    #to get files
    files=app.get_Files()
    
    if files[0]:#if no problem
       #to check if file we need exists
       for file in files[1]:
           if not os.path.exists(os.path.join(app.path_to_file,file)):
              return [False,"This {} files from files is missing please check ".format(file)]
       return [True,"All Files exists"]    
    else:
        return files
    
#to check if objets and expression are functionable    
def is_objests_Expression_functional():
    if app.get_Objets()[0] and app.get_Expressions()[0]:
        return [True,"Objects and Expression  are functional"]
    else:
        return [False,"Error in Objects and Expression "]

