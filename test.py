with open("test.txt","r") as f:
    lines = f.readlines()+["$%"]
spe_keywords = ["footer","fields","thumbnail","image"]
state = None
sub_state = None
embed = {
    "fields":[]
}
sub_state_check = False
previous_indentlevel = 0
extract = []
for index in range(len(lines)):
    line_indent = lines[index]
    indent = len(line_indent) - len(line_indent.lstrip())
    line = lines[index].lstrip().strip("\n").strip("\r")
    if len(line) == 0:
        continue
    if indent == 0:
        if line != "embed:" and line != "$%":
            extract.append(line)
        if state == "embed":
            extract.append(embed)
            embed = {
                "fields":[]
            }
            state = None
            sub_state = None
    if sub_state in spe_keywords and sub_state_check:
        if previous_indentlevel != indent:
            sub_state_check = False
            previous_indentlevel = 0

    if not state and line.split(":")[0] == "embed":
        state = "embed"
    elif state == "embed" and line.split(":")[0] in spe_keywords:
        sub_state = line.split(":")[0]
    elif state == "embed" and line.split(":")[0] not in spe_keywords and not sub_state:
        split = line.split(":",1)
        if split[0] == "color":
            embed[split[0]] = int(split[1],0)
        else:
            embed[split[0]] = split[1]
    elif sub_state in spe_keywords and not sub_state_check:
        pr = indent
        i = 0
        while True:
            if (index+i) > len(lines)-1:
                break
            indent_ = len(lines[index+i]) - len(lines[index+i].lstrip())
            
            if pr == indent_:
                pass
            else:
                break
            i+=1
        if sub_state == "fields":
            print(line)
            try:
                embed["fields"].append({
                    "name":lines[index:index+i][0].split(":")[1].lstrip(),
                    "value":lines[index:index+i][1].split(":",1)[1].lstrip()
                })
            except:pass
        else:
            embed[sub_state] = {
              i.lstrip().split(":")[0]:i.lstrip().split(":",1)[1] for i in lines[index:index+i]
            }
        sub_state_check = True
        previous_indentlevel = 0
        

print(extract)