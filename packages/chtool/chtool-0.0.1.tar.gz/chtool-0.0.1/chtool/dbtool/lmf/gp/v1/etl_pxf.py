from lmf.dbv2 import db_query,db_command 
import copy 
from collections import OrderedDict
import re ,time
class pg_to_gp:
    """para={"distri":None,"pxf_partition":None,'external_only':False,"exclude_col":None}
    """
    def __init__(self,conp_src,conp_dst):
        self.conp_src=copy.deepcopy(conp_src)
        self.conp_dst=copy.deepcopy(conp_dst)


    def copy(self,tb_src,tb_dst,coltext=None,**krg):
        bg=time.time()
        #"&PARTITION_BY=year:int&RANGE=2011:2013&INTERVAL=1"
        para={"distri":None,"pxf_partition":None,'external_only':False,"exclude_col":None,"rename":{},"drop":False}
        para.update(krg)

        user,passwd,host,db,schema=self.conp_src
        src_schema,src_name=tb_src.split('.')
        dst_schema,dst_name=tb_dst.split('.')

        #删除可能存在的外部表
        sql="select tablename from pg_tables where schemaname='%s' and tablename='%s_tmp' "%(dst_schema,dst_name)
        df=db_query(sql,dbtype="postgresql",conp=self.conp_dst)
        if not df.empty:
            sql="drop external table %s.%s_tmp"%(dst_schema,dst_name)
            print(sql)
            db_command(sql,dbtype="postgresql",conp=self.conp_dst)


        coltext=self.get_coltext(tb_src,coltext)
        col_type=[[re.split('\s+',w,1)[0].strip(),re.split('\s+',w,1)[1].strip() ] for w in re.split(",(?!\s*[0-9\)])",coltext)]
        data1=[]#外部表
        data2=[]#目的地表
        data3=[]

        arr=[] #insert 处的内容
        brr=[] #insert 处的select 内容
        exclude_col=[]
        rename=para['rename']
        if para['exclude_col'] is not None:
            exclude_col=[ w.strip() for w in para['exclude_col'].split(',') ]
        for w in col_type:
            if w[1] in ['json','tsvector','jsonb']:
                data1.append([w[0],'text'])
            elif w[1].startswith('_'):
                data1.append([w[0],'text'])
            else:
                data1.append(w)
            if w[0] not in exclude_col:
                data2.append(w)
                arr.append(w[0])
                if w[0] in rename.keys():
                    brr.append(rename[w[0]])
                else:
                    if w[1] in ['json','jsonb','tsvector']:
                        brr.append('%s::%s %s'%(w[0],w[1],w[0]))
                    elif w[1].startswith('_'):
                        brr.append("%s::%s %s"%(w[0],w[1],w[0]))
                    else:
                        brr.append(w[0])

        coltext_external=','.join([ ' '.join(w1) for w1 in data1])
        coltext_dsttb=','.join([ ' '.join(w1) for w1 in data2])
        #dst里创建外部表
        partition_by="" if para['pxf_partition'] is None else para['pxf_partition']
        sql="""
        create  external table %s.%s_tmp(%s) 
        LOCATION ('pxf://%s.%s?PROFILE=JDBC&JDBC_DRIVER=org.postgresql.Driver&DB_URL=jdbc:postgresql://%s/%s&USER=%s&PASS=%s%s')
        FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
        """%(dst_schema,dst_name,coltext_external,src_schema,src_name,host,db,user,passwd,partition_by)
        print(sql)
        db_command(sql,dbtype="postgresql",conp=self.conp_dst)


        ##只生成外部表
        if para['external_only']:
            print("只生成外部表")
            return 
        #select into 生成表
        if para['drop']:
            sql="drop table if exists  %s.%s"%(dst_schema,dst_name)
            print(sql)
            db_command(sql,dbtype="postgresql",conp=self.conp_dst)
        else:
            sql="truncate  %s.%s"%(dst_schema,dst_name)
            print(sql)
            db_command(sql,dbtype="postgresql",conp=self.conp_dst)


        colnames=','.join(arr)
        colnames1=','.join(brr)
        if para['distri'] is None:
            sql="""create table if not exists %s (%s ) """%(tb_dst,coltext_dsttb)
        else:
            sql="""create table if not exists %s (%s ) distributed by(%s) """%(tb_dst,coltext_dsttb,para['distri'])
        print(sql)
        db_command(sql,dbtype="postgresql",conp=self.conp_dst)
        
        sql="""insert into  %s(%s) select %s from %s_tmp """%(tb_dst,colnames,colnames1,tb_dst)
        print(sql)
        db_command(sql,dbtype="postgresql",conp=self.conp_dst)


        #删除外部表
        sql="select tablename from pg_tables where schemaname='%s' and tablename='%s_tmp' "%(dst_schema,dst_name)
        df=db_query(sql,dbtype="postgresql",conp=self.conp_dst)
        if not df.empty:
            sql="drop external table %s.%s_tmp"%(dst_schema,dst_name)
            print(sql)
            db_command(sql,dbtype="postgresql",conp=self.conp_dst)

        ed=time.time()
        cost=int(ed-bg)
        print("total--cost %d s"%cost)


    def get_coltext(self,tbname,coltext=None):
        schema,name=tbname.split(".")
        sql="""select
            col.ordinal_position,
            col.column_name,
            col.udt_name as data_type,
            col.character_maximum_length,
            col.numeric_precision,
            col.numeric_scale,
            col.is_nullable,
            col.column_default
            from
            information_schema.columns as col 
            where
            table_schema = '%s'
            and table_name = '%s'
            order by
            ordinal_position;
            """%(schema,name)
        df=db_query(sql,dbtype="postgresql",conp=self.conp_src)
        data=[]
        if coltext is not None:  
            coldict={ re.split('\s+',w,1)[0]:re.split('\s+',w,1)[1]  for w in re.split(",(?!\s*[0-9\)])",coltext)}
        else:
            coldict={}

        for i in range(len(df)):
            col_name,data_type,char_len,numeric_precision,numeric_scale=df.at[i,'column_name'],df.at[i,'data_type'],df.at[i,'character_maximum_length'],df.at[i,'numeric_precision'],df.at[i,'numeric_scale']
            if col_name in coldict.keys():
                data.append("%s %s"%(col_name,coldict[col_name]))
                continue 
            if data_type.startswith('_'):
                data.append("%s %s"%(col_name,data_type))
                continue 
            if 'char' in data_type:
                s="%s varchar"%(col_name) if char_len is None or str(char_len)=='nan' else "%s varchar(%s)"%(col_name,str(int(char_len)))
                data.append(s)
                continue 
            if 'numeric' in data_type:
                s="%s numeric"%(col_name) if numeric_precision is None or  str(numeric_precision)=='nan' else "%s numeric(%s,%s)"%(col_name,str(int(numeric_precision)),str(int(numeric_scale)) )
                data.append(s)
                continue 
            if 'double' in data_type or  'float' in data_type:
                s="%s float"%(col_name) 
                data.append(s)
                continue
            if data_type=='integer':
                s="%s int"%(col_name) 
                data.append(s)
                continue
            if 'json'==data_type:
                s="%s json"%(col_name) 
                data.append(s)
                continue
            if 'jsonb'==data_type:
                s="%s jsonb"%(col_name) 
                data.append(s)
                continue
            if 'timestamp' in data_type:
                s="%s timestamp(0)"%(col_name) 
                data.append(s)
                continue
            
            data.append("%s %s"%(col_name,data_type))

        coltext=','.join(data)

        return coltext


    def copy_exteral_only(self,tb_src,tb_dst,coltext=None,**krg):
        self.copy(tb_src,tb_dst,coltext=coltext,external_only=True,**krg)




if __name__=='__main__':
    conp_src=['postgres','since2015','172.16.0.9','zljianzhu','guangdong_qiye_zljianzhu']
    conp_dst=['gpadmin','since2015','172.16.0.10:5432','testdb','public']
    m=pg_to_gp(conp_src,conp_dst)
    m.copy('guangdong_qiye_zljianzhu.test11','public.test11',distri='a',exclude_col='name',drop=True)

