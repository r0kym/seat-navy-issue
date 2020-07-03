Search.setIndex({docnames:["apiserver","authentication","configuration","database","esi","index","openapi","scheduler","sni","teamspeak","todos","uac"],envversion:{"sphinx.domains.c":1,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":1,"sphinx.domains.index":1,"sphinx.domains.javascript":1,"sphinx.domains.math":2,"sphinx.domains.python":1,"sphinx.domains.rst":1,"sphinx.domains.std":1,"sphinx.ext.todo":2,"sphinx.ext.viewcode":1,sphinx:56},filenames:["apiserver.rst","authentication.rst","configuration.rst","database.rst","esi.rst","index.rst","openapi.rst","scheduler.rst","sni.rst","teamspeak.rst","todos.rst","uac.rst"],objects:{"sni.__main__":{main:[8,1,1,""],parse_command_line_arguments:[8,1,1,""]},"sni.api":{server:[0,0,0,"-"]},"sni.api.server":{does_not_exist_exception_handler:[0,1,1,""],exception_handler:[0,1,1,""],get_ping:[0,1,1,""],permission_error_handler:[0,1,1,""],print_openapi_spec:[0,1,1,""],requests_httperror_handler:[0,1,1,""],start:[0,1,1,""]},"sni.conf":{assert_is_set:[2,1,1,""],flatten_dict:[2,1,1,""],get:[2,1,1,""],load_configuration_file:[2,1,1,""]},"sni.db":{mongodb:[3,0,0,"-"]},"sni.db.mongodb":{init:[3,1,1,""],migrate:[3,1,1,""],migrate_ensure_root:[3,1,1,""],migrate_ensure_root_dyn_token:[3,1,1,""],migrate_ensure_root_per_token:[3,1,1,""],migrate_ensure_superuser_group:[3,1,1,""],on_pre_save:[3,1,1,""]},"sni.esi":{esi:[4,0,0,"-"],sso:[4,0,0,"-"],token:[4,0,0,"-"]},"sni.esi.esi":{"delete":[4,1,1,""],EsiPath:[4,2,1,""],get:[4,1,1,""],get_path_scope:[4,1,1,""],load_esi_openapi:[4,1,1,""],post:[4,1,1,""],put:[4,1,1,""],request:[4,1,1,""]},"sni.esi.esi.EsiPath":{DoesNotExist:[4,3,1,""],MultipleObjectsReturned:[4,3,1,""],http_method:[4,4,1,""],id:[4,4,1,""],objects:[4,4,1,""],path:[4,4,1,""],path_re:[4,4,1,""],scope:[4,4,1,""],version:[4,4,1,""]},"sni.esi.sso":{AuthorizationCodeResponse:[4,2,1,""],DecodedAccessToken:[4,2,1,""],decode_access_token:[4,1,1,""],get_access_token:[4,1,1,""],get_auth_url:[4,1,1,""],get_basic_authorization_code:[4,1,1,""],refresh_access_token:[4,1,1,""]},"sni.esi.sso.AuthorizationCodeResponse":{access_token:[4,4,1,""],expires_in:[4,4,1,""],refresh_token:[4,4,1,""],token_type:[4,4,1,""]},"sni.esi.sso.DecodedAccessToken":{azp:[4,4,1,""],character_id:[4,5,1,""],exp:[4,4,1,""],iss:[4,4,1,""],jti:[4,4,1,""],kid:[4,4,1,""],name:[4,4,1,""],owner:[4,4,1,""],scp:[4,4,1,""],sub:[4,4,1,""]},"sni.esi.token":{EsiAccessToken:[4,2,1,""],EsiRefreshToken:[4,2,1,""],get_access_token:[4,1,1,""],save_esi_tokens:[4,1,1,""]},"sni.esi.token.EsiAccessToken":{DoesNotExist:[4,3,1,""],MultipleObjectsReturned:[4,3,1,""],access_token:[4,4,1,""],created_on:[4,4,1,""],expires_on:[4,4,1,""],id:[4,4,1,""],objects:[4,4,1,""],owner:[4,4,1,""],scopes:[4,4,1,""]},"sni.esi.token.EsiRefreshToken":{DoesNotExist:[4,3,1,""],MultipleObjectsReturned:[4,3,1,""],created_on:[4,4,1,""],id:[4,4,1,""],objects:[4,4,1,""],owner:[4,4,1,""],refresh_token:[4,4,1,""],scopes:[4,4,1,""],updated_on:[4,4,1,""]},"sni.scheduler":{run_scheduled:[7,1,1,""]},"sni.uac":{clearance:[11,0,0,"-"],token:[11,0,0,"-"]},"sni.uac.clearance":{AbsoluteScope:[11,2,1,""],AbstractScope:[11,2,1,""],ClearanceModificationScope:[11,2,1,""],ESIScope:[11,2,1,""],are_in_same_alliance:[11,1,1,""],are_in_same_coalition:[11,1,1,""],are_in_same_corporation:[11,1,1,""],assert_has_clearance:[11,1,1,""],distance_penalty:[11,1,1,""],has_clearance:[11,1,1,""],reset_clearance:[11,1,1,""]},"sni.uac.clearance.AbsoluteScope":{has_clearance:[11,5,1,""],level:[11,4,1,""]},"sni.uac.clearance.AbstractScope":{has_clearance:[11,5,1,""]},"sni.uac.clearance.ClearanceModificationScope":{has_clearance:[11,5,1,""],level:[11,4,1,""]},"sni.uac.clearance.ESIScope":{has_clearance:[11,5,1,""],level:[11,4,1,""]},"sni.uac.token":{StateCode:[11,2,1,""],Token:[11,2,1,""],create_dynamic_app_token:[11,1,1,""],create_permanent_app_token:[11,1,1,""],create_state_code:[11,1,1,""],create_user_token:[11,1,1,""],from_authotization_header:[11,1,1,""],from_authotization_header_nondyn:[11,1,1,""],get_token_from_jwt:[11,1,1,""],to_jwt:[11,1,1,""]},"sni.uac.token.StateCode":{DoesNotExist:[11,3,1,""],MultipleObjectsReturned:[11,3,1,""],app_token:[11,4,1,""],created_on:[11,4,1,""],id:[11,4,1,""],objects:[11,4,1,""],uuid:[11,4,1,""]},"sni.uac.token.Token":{DoesNotExist:[11,3,1,""],MultipleObjectsReturned:[11,3,1,""],TokenType:[11,2,1,""],callback:[11,4,1,""],comments:[11,4,1,""],created_on:[11,4,1,""],expires_on:[11,4,1,""],id:[11,4,1,""],objects:[11,4,1,""],owner:[11,4,1,""],parent:[11,4,1,""],token_type:[11,4,1,""],uuid:[11,4,1,""]},"sni.uac.token.Token.TokenType":{_generate_next_value_:[11,5,1,""],_member_map_:[11,4,1,""],_member_names_:[11,4,1,""],_member_type_:[11,4,1,""],_value2member_map_:[11,4,1,""],dyn:[11,4,1,""],per:[11,4,1,""],use:[11,4,1,""]},"sni.user":{group:[11,0,0,"-"],user:[11,0,0,"-"]},"sni.user.group":{Group:[11,2,1,""],ensure_autogroup:[11,1,1,""]},"sni.user.group.Group":{DoesNotExist:[11,3,1,""],MultipleObjectsReturned:[11,3,1,""],created_on:[11,4,1,""],description:[11,4,1,""],id:[11,4,1,""],is_autogroup:[11,4,1,""],map_to_teamspeak:[11,4,1,""],members:[11,4,1,""],name:[11,4,1,""],objects:[11,4,1,""],owner:[11,4,1,""],teamspeak_sgid:[11,4,1,""],updated_on:[11,4,1,""]},"sni.user.user":{Alliance:[11,2,1,""],Coalition:[11,2,1,""],Corporation:[11,2,1,""],User:[11,2,1,""],ensure_alliance:[11,1,1,""],ensure_corporation:[11,1,1,""],ensure_user:[11,1,1,""]},"sni.user.user.Alliance":{DoesNotExist:[11,3,1,""],MultipleObjectsReturned:[11,3,1,""],alliance_id:[11,4,1,""],alliance_name:[11,4,1,""],coalitions:[11,5,1,""],executor:[11,5,1,""],executor_corporation_id:[11,4,1,""],id:[11,4,1,""],objects:[11,4,1,""],ticker:[11,4,1,""],updated_on:[11,4,1,""],user_iterator:[11,5,1,""],users:[11,5,1,""]},"sni.user.user.Coalition":{DoesNotExist:[11,3,1,""],MultipleObjectsReturned:[11,3,1,""],created_on:[11,4,1,""],id:[11,4,1,""],members:[11,4,1,""],name:[11,4,1,""],objects:[11,4,1,""],ticker:[11,4,1,""],updated_on:[11,4,1,""],user_iterator:[11,5,1,""],users:[11,5,1,""]},"sni.user.user.Corporation":{DoesNotExist:[11,3,1,""],MultipleObjectsReturned:[11,3,1,""],alliance:[11,4,1,""],ceo:[11,5,1,""],ceo_character_id:[11,4,1,""],corporation_id:[11,4,1,""],corporation_name:[11,4,1,""],id:[11,4,1,""],objects:[11,4,1,""],ticker:[11,4,1,""],updated_on:[11,4,1,""],user_iterator:[11,5,1,""],users:[11,5,1,""]},"sni.user.user.User":{DoesNotExist:[11,3,1,""],MultipleObjectsReturned:[11,3,1,""],character_id:[11,4,1,""],character_name:[11,4,1,""],clearance_level:[11,4,1,""],corporation:[11,4,1,""],created_on:[11,4,1,""],id:[11,4,1,""],is_ceo_of_alliance:[11,5,1,""],is_ceo_of_corporation:[11,5,1,""],objects:[11,4,1,""],teamspeak_cldbid:[11,4,1,""],tickered_name:[11,5,1,""],updated_on:[11,4,1,""]},sni:{__main__:[8,0,0,"-"],conf:[2,0,0,"-"],scheduler:[7,0,0,"-"],teamspeak:[9,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","function","Python function"],"2":["py","class","Python class"],"3":["py","exception","Python exception"],"4":["py","attribute","Python attribute"],"5":["py","method","Python method"]},objtypes:{"0":"py:module","1":"py:function","2":"py:class","3":"py:exception","4":"py:attribute","5":"py:method"},terms:{"24h":1,"2c48822e0a1b":4,"43c5":4,"478b":1,"48h":1,"4df0":1,"6eg8e7z4":2,"8pmzcetkb4vfudrhlc":4,"998e12c7":4,"abstract":11,"boolean":11,"byte":11,"catch":0,"class":[2,4,11],"default":[2,4,11],"enum":11,"function":7,"int":[4,11],"new":[4,11],"null":[4,11],"public":[4,11],"return":[3,4,11],"short":[4,11],"true":2,"try":[4,11],"while":11,EVE:[2,4,5,11],For:11,Not:2,That:0,The:[1,2,4,5,10,11],Then:5,There:1,Use:[4,11],Uses:[4,11],__main__:8,_cl:[4,11],_generate_next_value_:11,_member_map_:11,_member_names_:11,_member_type_:11,_request:0,_sender:[3,7],_value2member_map_:11,a8b9:1,about:11,absolut:11,absolutescop:11,abstractscop:11,access:[4,5],access_token:4,accur:[4,11],act:3,action:11,actual:11,added:[2,4,11],addit:11,admin:2,administr:11,aezxdswm:4,affili:5,after:[1,3],against:11,aka:11,algorithm:2,alia:11,all:[0,1,5,11],allianc:[4,10,11],alliance_id:11,alliance_nam:11,allow:[4,11],along:4,alreadi:[4,11],also:[1,2,11],altari:5,altern:[4,11],ani:[2,3,7,11],anoth:11,anyth:[3,4,11],api:[1,2,4,5],app:[1,2,3,5,11],app_token:11,appli:11,applic:[1,2,4,5,11],apschedul:7,are_in_same_alli:11,are_in_same_coalit:11,are_in_same_corpor:11,arg:[4,11],argpars:8,argument:[4,8,11],around:[4,11],arrai:11,asctim:2,assert:11,assert_has_clear:11,assert_is_set:2,asset:4,associ:[4,11],async:0,asyncron:7,auth:2,auth_group_nam:2,authent:[2,5,11],authentication_sourc:2,author:[1,4,11],authorizationcoderespons:4,automat:[2,4,11],avail:[4,11],azp:4,baee74e2d517:1,base:[4,11],basemodel:4,bash:5,bearer:[1,4,11],becaus:[4,11],been:7,befor:[4,11],bit:11,bloke:4,bookmark:4,bool:11,bot_nam:2,both:11,broken:[4,11],builtin:11,c_a:2,c_b_x:2,c_b_y:2,calendar:4,call:[3,4,7,11],callabl:7,callback:[5,11],can:[1,4,11],cannot:[4,11],cascad:[4,11],ceo:11,ceo_character_id:11,chang:[4,5,11],charact:[4,11],character_id:[1,4,11],character_nam:[7,11],characterstat:4,check:11,clearanc:5,clearance_level:11,clearancemodificationscop:11,client:2,client_id:[2,4],client_secret:[2,4],clone:4,coalit:[10,11],code:[4,5,11],collect:11,com:[2,4,5],command:8,comment:11,common:11,commun:4,complexdatetimefield:[4,11],compos:5,concurr:7,conf:2,config:2,configur:5,connect:3,connect_via:7,consid:[4,11],contain:[4,5,8,11],container_nam:5,contract:4,control:5,convert:[4,11],copror:11,corpor:[4,10,11],corporation_id:11,corporation_nam:11,correspond:11,count:11,creat:[2,3,4,5,7,11],create_dynamic_app_token:11,create_permanent_app_token:11,create_state_cod:11,create_user_token:11,created_on:[4,11],createus:5,credit:2,current:[3,4,11],data:[5,11],databas:[2,4,5,11],date:[4,11],datetim:[3,4,11],datetimefield:[4,11],dateutil:[4,11],dcbd81af:1,debug:[2,7],declar:11,decod:4,decode_access_token:4,decodedaccesstoken:4,decor:7,def:7,delet:[4,11],demot:11,deni:[4,11],depend:[4,11],derefer:[4,11],dereferenc:[4,11],deriv:[1,4,11],descript:11,determin:11,develop:[2,5],dict:2,dictfield:[4,11],dictionnari:2,differ:11,direct:[4,11],disable_existing_logg:2,distance_penalti:11,do_noth:[4,11],doc:4,docker:5,docstr:10,document:[0,3,7,8],doe:[2,3,4,11],does_not_exist_exception_handl:0,doesnotexist:[0,4,11],domain:5,don:[4,5,11],done:1,dyn:11,dynam:[1,3,11],each:11,easiest:5,editor:6,effect:[4,11],els:[7,11],embeddeddocu:[4,11],empti:[4,11],enabl:2,end:11,ensur:11,ensure_alli:[10,11],ensure_autogroup:11,ensure_corpor:[10,11],ensure_us:11,entri:[8,10],enumer:11,environ:5,error:[0,4,11],esi:[1,2,5,10,11],esi_respons:4,esi_scop:4,esiaccesstoken:4,esipath:4,esirefreshtoken:4,esiscop:11,especi:[4,11],etc:5,eveonlin:4,everyon:11,everytim:[4,11],evetech:4,exampl:[4,5,7],except:[0,2,4,11],exception_handl:0,exec:5,executor:11,executor_corporation_id:11,exist:[3,11],exp:4,expir:1,expires_in:4,expires_on:[4,11],ext:2,extract:4,eyjhbgcioijiuzi1niisin:1,facil:5,fals:[2,7,11],fastapi:11,featur:[4,11],fetch:11,field:[4,11],file:[2,5,6],fit:4,flatten:2,flatten_dict:2,fleet:4,follow:5,forget:5,form:[1,4],formal:11,format:[2,4,11],formatt:2,forward:0,found:4,from:[1,2,4,11],from_authotization_head:11,from_authotization_header_nondyn:11,fulli:[4,11],furthermor:11,gener:2,get:[1,2,4,7,11],get_access_token:[4,10],get_auth_url:4,get_basic_authorization_cod:4,get_p:0,get_path_scop:4,get_token_from_jwt:11,git:5,git_url:5,github:[5,10],given:[4,11],global:[0,7,11],grant:11,group:[2,3,5,10],handl:[4,11],handler:[0,2],happen:[4,11],has:[3,7,11],has_clear:11,have:[2,6,11],header:[1,11],here:[2,6],hex:2,hierarch:11,his:11,host:2,how:11,hs256:2,html:4,http:[2,4,5,11],http_method:4,httperror:0,idididididididididididididididid:2,imag:5,immedi:[3,7],implement:[4,11],imran:2,inact:1,includ:1,index:5,indic:11,industri:4,info:2,inform:11,inherit:1,init:3,initi:[3,4],input:11,instal:[4,11],instanc:[3,4,11],instead:11,integ:11,interfac:4,invalid:11,invaliddocumenterror:[4,11],is_autogroup:11,is_ceo_of_alli:11,is_ceo_of_corpor:11,iss:4,issu:[2,4,11],iter:11,its:[4,11],job:[3,7],json:4,jti:4,jwt:[1,2,4,10,11],jzozkrta8b:4,kei:[2,4],kid:4,killmail:4,kind:1,known:[4,11],kwarg:[4,7],last_valu:11,latest:4,layer:[3,5],lazili:[4,11],lazyreferencefield:[4,11],lead:[4,11],least:11,level:2,levelnam:2,librari:[4,11],like:[1,4,11],line:[8,10],list:[4,5,11],listfield:[4,11],load:[2,4],load_configuration_fil:2,load_esi_openapi:4,locat:[2,4,10],log:[1,2,7,11],logger:2,login:4,look:[1,4],lqjg2:4,magic:3,mail:4,main:[4,5],maintain:[10,11],make:[3,4,7],manag:[4,7,11],manage_planet:4,mani:[4,11],manual:[1,11],map_to_teamspeak:11,mapfield:[4,11],market:4,match:5,matter:11,mean:[4,11],member:[7,11],messag:2,metadata:[4,11],method:11,microsecond:[4,11],migrat:3,migrate_ensure_root:3,migrate_ensure_root_dyn_token:3,migrate_ensure_root_per_token:3,migrate_ensure_superuser_group:3,millisecond:[4,11],mode:2,model:[0,1,4,11],mongo:5,mongo_initdb_root_password:5,mongo_initdb_root_usernam:5,mongodb:[2,4,5,11],mongoengin:[0,3,4,11],more:4,most:11,multipl:[4,10,11],multipleobjectsreturn:[4,11],must:[1,11],mutablemap:2,my3rdpartyclientid:4,name:[2,4,11],namespac:8,navi:2,nearest:[4,11],necessari:[4,11],need:[4,11],nested_dict:2,net:4,none:[0,2,3,4,11],note:[1,4,11],notif:1,notimplementederror:11,nullifi:[4,11],oauth:4,object:[4,11],objectid:[4,11],obtain:1,on_pre_sav:3,onc:1,one:[4,11],onli:[4,11],open_window:4,openapi:[0,4,5],openssl:2,option:[4,11],order:1,org:[4,11],organize_mail:4,origin:[5,10],other:[0,11],otherwis:11,over:11,own:[3,11],owner:[3,4,11],page:5,pagin:[10,11],paramet:4,parent:11,parent_kei:2,pars:[4,8,11],parse_command_line_argu:8,parser:[4,11],part:11,pass:4,password:[2,5],path:[2,4],path_r:4,per:11,perform:[4,11],perman:[1,3,11],permission_error_handl:0,permissionerror:[0,11],planet:4,point:8,pong:0,poor:[4,11],port:2,portal:[2,5],post:4,post_sav:7,postcallbackesiout:1,posttokenusefromdynout:1,postusefromperout:1,pre:[4,11],precis:[4,11],prefix:11,present:[4,11],preserv:11,pretermin:11,prevent:[4,11],print:0,print_openapi_spec:0,priviledg:11,privileg:1,propag:2,properti:[4,11],provid:11,publicdata:4,pull:[4,11],pumba:5,pure:11,put:4,pwd:5,pydant:4,pyjwt:2,python:[4,11],python_main_modul:5,queri:2,rais:[2,4,11],rand:2,read:[4,11],read_agents_research:4,read_asset:4,read_blueprint:4,read_calendar_ev:4,read_character_bookmark:4,read_character_contract:4,read_character_job:4,read_character_min:4,read_character_ord:4,read_character_wallet:4,read_chat_channel:4,read_clon:4,read_contact:4,read_container_log:4,read_corporation_asset:4,read_corporation_bookmark:4,read_corporation_contract:4,read_corporation_job:4,read_corporation_killmail:4,read_corporation_membership:4,read_corporation_min:4,read_corporation_ord:4,read_corporation_rol:4,read_corporation_wallet:4,read_customs_offic:4,read_divis:4,read_facil:4,read_fatigu:4,read_fit:4,read_fleet:4,read_fw_stat:4,read_impl:4,read_killmail:4,read_loc:4,read_loyalti:4,read_mail:4,read_med:4,read_notif:4,read_onlin:4,read_opportun:4,read_ship_typ:4,read_skil:4,read_skillqueu:4,read_stand:4,read_starbas:4,read_structur:4,read_titl:4,readwrit:5,redi:[2,5],refer:[3,4,5,11],referenc:[4,11],referencefield:[4,11],refresh:4,refresh_access_token:4,refresh_token:4,regis:11,regist:[4,5,11],register_delete_rul:[4,11],relat:11,relev:[4,11],remeb:11,repli:0,repons:4,repres:[4,11],represent:11,request:[0,1,5],requests_httperror_handl:0,requir:[1,4,5,11],reset:11,reset_clear:11,respond_calendar_ev:4,respons:[1,4],result:[10,11],retriev:[4,11],reverse_delete_rul:[4,11],revok:1,rguc:4,role:5,root:[1,2,3,5,11],root_url:2,rootpassword:5,round:[4,11],router:[1,5],rule:[4,11],run:[0,3,7],run_schedul:7,same:11,save:[4,11],save_esi_token:4,schedul:5,scheduler_thread_count:2,scope:[5,10,11],scope_level:11,scope_nam:11,scp:4,search:[4,5],search_structur:4,seat:2,secret:2,secretsecretsecretsecretsecretsecret0000:2,secretsecretsecretsecretsecretsecretsecretsecretsecretsecret0000:2,see:[1,2,4,5,11],send_mail:4,sent:1,separ:2,server:[2,5],server_id:2,servic:5,set:[2,3,4,11],shell:5,should:[1,3,4,11],signal:7,signatur:4,simpli:[7,11],singl:11,skill:4,sni:[1,2,3,7,8,10],snipassword:[2,5],solv:[4,11],some:[4,11],sourc:[0,2,3,4,7,8,11],specif:[0,4,5,11],src:5,sso:[1,10,11],stage:4,standard:[2,4,11],start:[0,11],state:[4,11],state_cod:1,statecod:11,statu:7,stdout:2,str:[2,4,11],stream:2,streamhandl:2,string:[4,11],strptime:[4,11],structure_market:4,sub:4,subsequ:1,suffici:11,suitabl:4,superior:11,superus:[3,11],support:[2,4,10,11],sure:3,swagger:[4,6],syntax:[4,11],sys:2,take:1,target:11,task:11,teamspeak:[2,5],teamspeak_cldbid:11,teamspeak_sgid:11,tell:11,test:7,than:11,thei:11,them:0,themselv:1,thi:[1,2,4,8,11],through:2,ticker:11,tickered_nam:11,tied:1,time:[4,11],tkn:11,to_jwt:11,todo:5,token:[1,3,10],token_str:11,token_typ:[4,11],tokentyp:11,trace:0,track_memb:4,two:[1,11],type:[4,11],uac:5,under:1,unicod:[4,11],univers:4,updat:[4,7,11],updated_on:[3,4,11],url:[2,4,11],urlsafe_b64encod:4,use:[1,4,5,7,11],used:[2,4,11],useful:[4,11],user1:11,user2:11,user:[1,2,3,4,5,7,10],user_iter:11,user_token:1,usernam:[2,5],using:[4,11],usr:[5,7,11],utc:[4,11],utcnow:[4,11],util:11,utilis:[4,11],uuid:11,valid:[1,4,10,11],valu:[2,4,11],vari:[4,11],variou:[3,11],verif:11,version:[2,4,5,11],via:1,virtual:11,volum:5,wai:[5,11],wallet:4,warn:11,web:4,web_based_sso_flow:4,wether:11,what:[4,11],when:[4,7,11],which:[1,2,4,11],whichev:11,wish:1,workspac:10,wrap:[4,11],wrapper:[4,11],write:11,write_contact:4,write_fit:4,write_fleet:4,write_waypoint:4,yaml:[0,2,6],yml:[2,5],you:[4,11],your:5},titles:["API Server","Authentication","Configuration facility","Database modules","ESI requests layer","SeAT Navy Issue","OpenAPI specification","Scheduler","Main module","Teamspeak module","Todo list","User Access Control"],titleterms:{access:11,api:0,authent:1,clearanc:11,coalit:0,configur:2,control:11,databas:3,document:[2,4,5,9,11],esi:[0,4],etc:11,exampl:2,facil:2,group:[0,11],high:5,indic:5,issu:5,layer:4,level:[5,11],list:10,main:[0,8],modul:[0,2,3,4,5,8,9,11],mongodb:3,navi:5,openapi:6,redi:3,refer:2,request:4,router:0,run:5,schedul:7,scope:4,seat:5,server:0,sni:[0,4,5,11],specif:6,sso:4,tabl:5,teamspeak:[0,9],todo:[4,10,11],token:[0,4,11],uac:11,user:[0,11]}})