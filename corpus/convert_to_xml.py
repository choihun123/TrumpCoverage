import json
import os

from dicttoxml import dicttoxml

def main():
    filenames = os.listdir("last-json")
    trump_json_filenames = [filename for filename in filenames if '_trump.json' in filename]
    cur_dir = os.getcwd()
    json_dir = os.path.join(cur_dir, "last-json")
    xml_dir = os.path.join(cur_dir, "xml")
    for filename in trump_json_filenames:
        
        file_path = os.path.join(json_dir, filename)
        with open(file_path) as fp:
            data = json.loads(fp.read())
                    
        
        new_dict_list = [
            {'id': d['id'], 'newspaper_article_text': d['newspaper_article_text']}
            for d in data
        ]
        
        xml = dicttoxml(new_dict_list)o
        import xml.etree.ElementTree as ET
        with open('/tmp/x.xml', 'w+') as fp:
            fp.write(xml)
        et = ET.parse('/tmp/x.xml')
        
        print filename, len(data), len(et.getroot().getchildren())
        base_filename = filename.split('.json')[0]
        xml_filename = base_filename + '.xml'
        xml_file_path = os.path.join(xml_dir, xml_filename)
        with open(xml_file_path, 'w+') as fp:
            fp.write(xml)


if __name__ == '__main__':
    main()

