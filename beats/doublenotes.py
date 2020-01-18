#doublenotes.py

name = input("name: ")

same = [] #if the note is the same, it appends to this list

for beat in open("%s_beatz.txt"%(name),"r"):
    beat = beat.strip()
    note,time = beat.split(":")
    same.append([note,time])

for i in range(len(same)):
    for j in range(len(same[i])):
