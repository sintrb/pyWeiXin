# -*- coding: UTF-8 -*
'''
Convertting with XML and Python Dictionary.

Created on 2013-9-3

@author: RobinTang

GitHub: https://github.com/sintrb/pyxmldict


Dictionary to XML:
When diction has a array, such as:
{
    'items':[1,2,3]
}

Will be converted to:
<xml>
 <items>
  <item>1</item>
  <item>2</item>
  <item>3</item>
 </items>
</xml>

That is, items's children's tag is 'item'.
For example, if array's name is 'values', then children's tag will be 'value'.


'''

import types


__VERSION__ = '1.0'

def __val2xml__(val):
    '''
    Convert a Python value to XML element 
    '''
    if type(val) is types.IntType or type(val) is types.FloatType:
        return val
    else:
        return '<![CDATA[%s]]>'%str(val)


__INDENT__ = ' '  # Indentation for each XNL line, no indentation when empty.
__NEWLINE__ = '\n'  # New line char, no new line when empty
__VAL2XML__ = __val2xml__  # Python value to XML element, if unnecessary set it with str function: __VAL2XML__ = str



def __obj2xml__(tag, obj, pres='', newline=__NEWLINE__):
    '''
    convert object to XML
    '''
    tp = type(obj)
    if tp is types.DictType:
        return '%s<%s>%s%s%s%s</%s>' % (pres, tag, newline, newline.join([__obj2xml__(k, v, pres + __INDENT__, newline) for k, v in obj.items()]), newline, pres, tag)
    elif tp is types.TupleType or tp is types.ListType:
        return '%s<%s>%s%s%s%s</%s>' % (pres, tag, newline, newline.join([__obj2xml__(tag[:-1], o, pres + __INDENT__, newline) for o in obj]), newline, pres, tag)
    else:
        return '%s<%s>%s</%s>' % (pres, tag, __VAL2XML__(obj), tag)

def dict2xml(obj):
    '''
    convert dictionary to XML
    '''
    return __obj2xml__('xml', obj)


def test():
    '''
    test case
    '''
    
    # test dictionary to XML
    print dict2xml(
    {
    'a':'aa',
    'b':'bb',
    'c':{
        'c1':'cc1',
        'c2':'cc2',
    'c3':{
        'c33':'C33',
        'c44':'C44',
    }
    },
    'items':[
        {'name':'item1', 'id':'id1'},
        {'name':'item2', 'id':'id2'},
        {'name':'item3', 'id':'id3'},
    ],
    'd':{
        'e':{
            'f':{
                'g':{
                    'h':'H'}}}},
     'name':'trb'
    }
    )

if __name__ == '__main__':
    test()
    



