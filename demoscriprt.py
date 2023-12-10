import pickle
import pdb
org_list = pickle.load(open("org.p","rb"))
for _,org in org_list.getObjectList().items():
    org.listObjects()