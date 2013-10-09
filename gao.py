# -*- coding:gbk -*-
import chunk2fbx
import primitives2fbx
import sys

def PrintHint(pString, pFlag = False):
    Hint = '#'
    if pFlag:
        Hint = '*'
    print Hint * 15 + '\n' + pString + '\n' + Hint * 15

def main():

    List = sys.argv[1:]

    cnt1 = cnt2 = 0
    for Listitem in List:
        if Listitem.endswith('.cdata') or Listitem.endswith('.chunk'):
            cnt1 += 1
        else:
            cnt2 += 1
    if cnt1 and cnt2:
        PrintHint('import error\nyou can only import primitives[dirname or filename] or (chunkname and cdataname)', True)
        raw_input('press enter to exit...')
        sys.exit(-1)
    if cnt1:
        #try:
        chunk2fbx.main(List)
        #except:
        #    PrintHint('Chunk To Fbx Error', True)
        #    raw_input('press enter to exit')
        #    sys.exit(-1)
    elif cnt2:
        #try:
        primitives2fbx.main(List)
       # except:
       #     PrintHint('Primitives To Fbx Error', True)
       #     raw_input('press enter to exit')
       #     sys.exit(-1)
    raw_input('#' * 15 + '\nsuccessfully!~\n' + '#' * 15 + '\npress enter to exit')
main()
