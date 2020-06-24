Search.setIndex({docnames:["apiserver","authentication","configuration","database","esi","index","openapi","scheduler","sni","todos","uac"],envversion:{"sphinx.domains.c":1,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":1,"sphinx.domains.index":1,"sphinx.domains.javascript":1,"sphinx.domains.math":2,"sphinx.domains.python":1,"sphinx.domains.rst":1,"sphinx.domains.std":1,"sphinx.ext.todo":2,"sphinx.ext.viewcode":1,sphinx:56},filenames:["apiserver.rst","authentication.rst","configuration.rst","database.rst","esi.rst","index.rst","openapi.rst","scheduler.rst","sni.rst","todos.rst","uac.rst"],objects:{"sni.__main__":{main:[8,1,1,""],parse_command_line_arguments:[8,1,1,""],start_api_server:[8,1,1,""]},"sni.apiserver":{does_not_exist_exception_handler:[0,1,1,""],exception_handler:[0,1,1,""],get_ping:[0,1,1,""],permission_error_handler:[0,1,1,""],print_openapi_spec:[0,1,1,""]},"sni.conf":{assert_is_set:[2,1,1,""],flatten_dict:[2,1,1,""],get:[2,1,1,""],load_configuration_file:[2,1,1,""]},"sni.db":{init:[3,1,1,""],migrate:[3,1,1,""],migrate_ensure_root:[3,1,1,""],migrate_ensure_root_dyn_token:[3,1,1,""],migrate_ensure_root_per_token:[3,1,1,""],migrate_ensure_superuser_group:[3,1,1,""]},"sni.esi":{esi:[4,0,0,"-"],sso:[4,0,0,"-"],token:[4,0,0,"-"]},"sni.esi.esi":{"delete":[4,1,1,""],EsiPath:[4,2,1,""],get:[4,1,1,""],get_path_scope:[4,1,1,""],load_esi_openapi:[4,1,1,""],post:[4,1,1,""],put:[4,1,1,""],request:[4,1,1,""]},"sni.esi.esi.EsiPath":{DoesNotExist:[4,3,1,""],MultipleObjectsReturned:[4,3,1,""],http_method:[4,4,1,""],id:[4,4,1,""],objects:[4,4,1,""],path:[4,4,1,""],path_re:[4,4,1,""],scope:[4,4,1,""],version:[4,4,1,""]},"sni.esi.sso":{AuthorizationCodeResponse:[4,2,1,""],DecodedAccessToken:[4,2,1,""],decode_access_token:[4,1,1,""],get_access_token:[4,1,1,""],get_auth_url:[4,1,1,""],get_basic_authorization_code:[4,1,1,""],refresh_access_token:[4,1,1,""]},"sni.esi.sso.AuthorizationCodeResponse":{access_token:[4,4,1,""],expires_in:[4,4,1,""],refresh_token:[4,4,1,""],token_type:[4,4,1,""]},"sni.esi.sso.DecodedAccessToken":{azp:[4,4,1,""],character_id:[4,5,1,""],exp:[4,4,1,""],iss:[4,4,1,""],jti:[4,4,1,""],kid:[4,4,1,""],name:[4,4,1,""],owner:[4,4,1,""],scp:[4,4,1,""],sub:[4,4,1,""]},"sni.esi.token":{EsiAccessToken:[4,2,1,""],EsiRefreshToken:[4,2,1,""],get_access_token:[4,1,1,""],save_esi_tokens:[4,1,1,""]},"sni.esi.token.EsiAccessToken":{DoesNotExist:[4,3,1,""],MultipleObjectsReturned:[4,3,1,""],access_token:[4,4,1,""],created_on:[4,4,1,""],expires_on:[4,4,1,""],id:[4,4,1,""],objects:[4,4,1,""],owner:[4,4,1,""],scopes:[4,4,1,""]},"sni.esi.token.EsiRefreshToken":{DoesNotExist:[4,3,1,""],MultipleObjectsReturned:[4,3,1,""],created_on:[4,4,1,""],id:[4,4,1,""],objects:[4,4,1,""],owner:[4,4,1,""],refresh_token:[4,4,1,""],scopes:[4,4,1,""],updated_on:[4,4,1,""]},"sni.routers":{esi:[0,0,0,"-"],token:[0,0,0,"-"]},"sni.routers.esi":{EsiRequestIn:[0,2,1,""],EsiRequestOut:[0,2,1,""],PostCallbackEsiOut:[0,2,1,""],get_callback_esi:[0,1,1,""],get_esi_latest:[0,1,1,""]},"sni.routers.esi.EsiRequestIn":{on_behalf_of:[0,4,1,""],params:[0,4,1,""]},"sni.routers.esi.EsiRequestOut":{data:[0,4,1,""],headers:[0,4,1,""],status_code:[0,4,1,""]},"sni.routers.esi.PostCallbackEsiOut":{state_code:[0,4,1,""],user_token:[0,4,1,""]},"sni.routers.token":{GetTokenOut:[0,2,1,""],PostTokenDynIn:[0,2,1,""],PostTokenDynOut:[0,2,1,""],PostTokenPerIn:[0,2,1,""],PostTokenPerOut:[0,2,1,""],PostTokenUseFromDynIn:[0,2,1,""],PostTokenUseFromDynOut:[0,2,1,""],PostUseFromPerOut:[0,2,1,""],delete_token:[0,1,1,""],get_token:[0,1,1,""],post_token_dyn:[0,1,1,""],post_token_per:[0,1,1,""],post_token_use_from_dyn:[0,1,1,""],post_token_use_from_per:[0,1,1,""]},"sni.routers.token.GetTokenOut":{callback:[0,4,1,""],comments:[0,4,1,""],created_on:[0,4,1,""],expires_on:[0,4,1,""],owner_character_id:[0,4,1,""],parent:[0,4,1,""],token_type:[0,4,1,""],uuid:[0,4,1,""]},"sni.routers.token.PostTokenDynIn":{callback:[0,4,1,""],comments:[0,4,1,""]},"sni.routers.token.PostTokenDynOut":{app_token:[0,4,1,""]},"sni.routers.token.PostTokenPerIn":{callback:[0,4,1,""],comments:[0,4,1,""]},"sni.routers.token.PostTokenPerOut":{app_token:[0,4,1,""]},"sni.routers.token.PostTokenUseFromDynIn":{scopes:[0,4,1,""]},"sni.routers.token.PostTokenUseFromDynOut":{login_url:[0,4,1,""],state_code:[0,4,1,""]},"sni.routers.token.PostUseFromPerOut":{user_token:[0,4,1,""]},"sni.uac":{clearance:[10,0,0,"-"],token:[10,0,0,"-"],user:[10,0,0,"-"]},"sni.uac.clearance":{are_in_same_alliance:[10,1,1,""],are_in_same_coalition:[10,1,1,""],are_in_same_corporation:[10,1,1,""],assert_has_clearance:[10,1,1,""],distance_penalty:[10,1,1,""],has_clearance:[10,1,1,""]},"sni.uac.token":{StateCode:[10,2,1,""],Token:[10,2,1,""],create_dynamic_app_token:[10,1,1,""],create_permanent_app_token:[10,1,1,""],create_state_code:[10,1,1,""],create_user_token:[10,1,1,""],get_token_from_jwt:[10,1,1,""],to_jwt:[10,1,1,""],validate_header:[10,1,1,""]},"sni.uac.token.StateCode":{DoesNotExist:[10,3,1,""],MultipleObjectsReturned:[10,3,1,""],app_token:[10,4,1,""],created_on:[10,4,1,""],id:[10,4,1,""],objects:[10,4,1,""],uuid:[10,4,1,""]},"sni.uac.token.Token":{DoesNotExist:[10,3,1,""],MultipleObjectsReturned:[10,3,1,""],TokenType:[10,2,1,""],callback:[10,4,1,""],comments:[10,4,1,""],created_on:[10,4,1,""],expires_on:[10,4,1,""],id:[10,4,1,""],objects:[10,4,1,""],owner:[10,4,1,""],parent:[10,4,1,""],token_type:[10,4,1,""],uuid:[10,4,1,""]},"sni.uac.token.Token.TokenType":{_generate_next_value_:[10,5,1,""],_member_map_:[10,4,1,""],_member_names_:[10,4,1,""],_member_type_:[10,4,1,""],_value2member_map_:[10,4,1,""],dyn:[10,4,1,""],per:[10,4,1,""],use:[10,4,1,""]},"sni.uac.user":{Alliance:[10,2,1,""],Coalition:[10,2,1,""],Corporation:[10,2,1,""],Group:[10,2,1,""],User:[10,2,1,""],ensure_alliance:[10,1,1,""],ensure_auto_group:[10,1,1,""],ensure_corporation:[10,1,1,""],ensure_user:[10,1,1,""]},"sni.uac.user.Alliance":{DoesNotExist:[10,3,1,""],MultipleObjectsReturned:[10,3,1,""],alliance_id:[10,4,1,""],alliance_name:[10,4,1,""],executor:[10,5,1,""],executor_corporation_id:[10,4,1,""],id:[10,4,1,""],objects:[10,4,1,""],ticker:[10,4,1,""]},"sni.uac.user.Coalition":{DoesNotExist:[10,3,1,""],MultipleObjectsReturned:[10,3,1,""],created_on:[10,4,1,""],id:[10,4,1,""],members:[10,4,1,""],name:[10,4,1,""],objects:[10,4,1,""],ticker:[10,4,1,""],updated_on:[10,4,1,""]},"sni.uac.user.Corporation":{DoesNotExist:[10,3,1,""],MultipleObjectsReturned:[10,3,1,""],alliance:[10,4,1,""],ceo:[10,5,1,""],ceo_character_id:[10,4,1,""],corporation_id:[10,4,1,""],corporation_name:[10,4,1,""],id:[10,4,1,""],objects:[10,4,1,""],ticker:[10,4,1,""]},"sni.uac.user.Group":{DoesNotExist:[10,3,1,""],MultipleObjectsReturned:[10,3,1,""],created_on:[10,4,1,""],description:[10,4,1,""],id:[10,4,1,""],members:[10,4,1,""],name:[10,4,1,""],objects:[10,4,1,""],owner:[10,4,1,""],updated_on:[10,4,1,""]},"sni.uac.user.User":{DoesNotExist:[10,3,1,""],MultipleObjectsReturned:[10,3,1,""],character_id:[10,4,1,""],character_name:[10,4,1,""],clearance_level:[10,4,1,""],corporation:[10,4,1,""],created_on:[10,4,1,""],id:[10,4,1,""],objects:[10,4,1,""]},sni:{__main__:[8,0,0,"-"],apiserver:[0,0,0,"-"],conf:[2,0,0,"-"],db:[3,0,0,"-"],scheduler:[7,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","function","Python function"],"2":["py","class","Python class"],"3":["py","exception","Python exception"],"4":["py","attribute","Python attribute"],"5":["py","method","Python method"]},objtypes:{"0":"py:module","1":"py:function","2":"py:class","3":"py:exception","4":"py:attribute","5":"py:method"},terms:{"24h":1,"2c48822e0a1b":4,"43c5":4,"478b":1,"48h":1,"4df0":1,"8pmzcetkb4vfudrhlc":4,"998e12c7":4,"byte":10,"case":10,"catch":0,"class":[0,2,4,10],"default":[2,4,10],"enum":10,"function":[4,10],"int":[0,4,10],"new":[0,4,10],"null":[4,10],"public":[4,10],"return":[0,3,4,10],"short":[4,10],"true":2,"try":[4,10],"while":10,EVE:[0,2,4,5,10],For:10,The:[1,2,4,5,9,10],Then:5,There:1,Use:[4,10],Uses:[4,10],__main__:8,_cl:[4,10],_generate_next_value_:10,_member_map_:10,_member_names_:10,_member_type_:10,_request:0,_value2member_map_:10,a8b9:1,about:[0,10],accept:[4,10],access:[4,5],access_token:4,accur:[4,10],act:3,action:10,actual:10,add:[4,10],added:[4,10],admin:2,administr:10,aezxdswm:4,affili:5,after:[1,3],against:10,aka:10,algorithm:2,alia:10,all:[0,1,5,10],allianc:[4,9,10],alliance_id:10,alliance_nam:10,allow:[4,10],along:4,alreadi:[4,10],also:[1,2,10],altari:5,altern:[4,10],ani:[0,2,3,4,10],anyhttpurl:0,anyth:[3,4,10],api:[1,2,4,5,8],apimodel:0,apiserv:0,app:[0,1,2,3,5,10],app_token:[0,10],applic:[0,1,2,4,5,10],apschedul:7,are_in_same_alli:10,are_in_same_coalit:10,are_in_same_corpor:10,arg:[4,10],argpars:8,argument:[4,8,10],around:[4,10],arrai:10,asctim:2,assert_has_clear:[9,10],assert_is_set:2,asset:4,associ:[4,10],async:0,asyncron:7,authent:[0,5,10],authentication_sourc:2,author:[1,4,10],authorizationcoderespons:4,automat:[4,10],avail:[4,10],azp:4,baee74e2d517:1,base:[0,4,10],basemodel:[0,4],bash:5,bearer:[1,4,10],becaus:[4,10],befor:[4,10],being:0,bit:10,bloke:4,bookmark:4,bool:10,both:10,broken:[4,10],builtin:10,c_a:2,c_b_x:2,c_b_y:2,calcul:10,calendar:4,call:[0,3,4,9,10],callback:[0,5,10],can:[0,1,4,10],cannot:[4,10],car:10,cascad:[4,10],ceo:10,ceo_character_id:10,chang:[4,5,10],charact:[4,10],character_id:[1,4,10],character_nam:10,characterstat:4,check:10,clearanc:[5,9],clearance_level:10,client_id:[2,4],client_secret:[2,4],clone:4,coalit:10,code:[0,4,5,9,10],collect:10,com:[2,4,5],command:8,comment:[0,10],common:10,commun:4,complexdatetimefield:[4,10],compos:5,concurr:7,conf:2,config:2,configur:5,connect:3,consid:[4,10],contain:[4,5,8,10],container_nam:5,contract:4,control:5,convert:[4,10],corpor:[4,9,10],corporation_id:10,corporation_nam:10,correspond:10,count:10,creat:[0,2,3,4,5,10],create_dynamic_app_token:10,create_permanent_app_token:10,create_state_cod:10,create_user_token:10,created_on:[0,4,10],createus:5,credit:2,current:[0,4,10],custom:[4,10],data:[0,5,10],databas:[2,4,5,10],date:[4,10],datetim:[0,4,10],datetimefield:[4,10],dateutil:[4,10],dcbd81af:1,debug:2,declar:10,decod:4,decode_access_token:4,decodedaccesstoken:4,delet:[0,4,10],delete_token:0,demot:10,deni:[4,10],depend:[0,4,10],derefer:[4,10],dereferenc:[4,10],deriv:[1,4,10],descript:10,develop:[2,5],dict:[0,2],dictfield:[4,10],dictionnari:2,differ:10,direct:[4,10],disable_existing_logg:2,distanc:10,distance_penalti:10,do_noth:[4,10],doc:4,docker:5,docstr:9,document:[0,3,7,8],doe:[2,3,4,10],does_not_exist_exception_handl:0,doesnotexist:[0,4,10],domain:5,don:[4,5,10],done:[0,1],dyn:[0,10],dynam:[0,1,3,10],each:10,easiest:5,editor:6,effect:[4,10],els:10,embeddeddocu:[4,10],empti:[4,10],end:10,ensur:10,ensure_alli:[9,10],ensure_auto_group:10,ensure_corpor:[9,10],ensure_us:10,entri:[8,9],enumer:10,environ:5,error:[0,4,9,10],esi:[1,2,5,9,10],esi_path:0,esi_respons:4,esi_scop:4,esiaccesstoken:4,esipath:4,esirefreshtoken:4,esirequestin:0,esirequestout:0,especi:[4,10],etc:5,eveonlin:4,everyon:10,everytim:[4,10],evetech:4,exampl:[4,5],except:[0,2,4,10],exception_handl:0,exec:5,executor:10,executor_corporation_id:10,exist:[3,10],exp:4,expir:1,expires_in:4,expires_on:[0,4,10],ext:2,extend:[4,10],extra:[4,10],extract:4,eyjhbgcioijiuzi1niisin:1,facil:5,factor:10,fals:[2,10],far:10,fastapi:10,featur:[4,10],fetch:10,field:[4,10],file:[2,5,6],first:[4,10],fit:4,flatten:2,flatten_dict:2,fleet:4,follow:5,forget:5,form:[1,4,10],formal:10,format:[2,4,10],formatt:2,formula:10,forward:0,found:4,from:[0,1,2,4,10],fulli:[4,10],furthermor:10,gener:2,get:[0,1,2,4,10],get_access_token:[4,9],get_auth_url:4,get_basic_authorization_cod:4,get_callback_esi:0,get_esi_latest:0,get_p:0,get_path_scop:4,get_token:0,get_token_from_jwt:10,gettokenout:0,git:5,git_url:5,github:[5,9],given:[4,10],global:[0,7],group:[3,5,9],handl:[4,10],handler:[0,2],happen:[4,10],has:10,has_clear:10,have:[2,6,10],header:[0,1,10],here:[2,6],hex:2,his:10,host:2,how:10,hs256:2,html:4,http:[2,4,5,10],http_method:4,idididididididididididididididid:2,imag:5,immedi:3,implement:[4,9,10],imran:2,inact:1,includ:1,index:5,industri:4,info:2,inform:[0,10],inherit:1,init:3,initi:[3,4],input:10,instal:[4,10],instanc:[3,4,10],integ:10,interfac:4,invaliddocumenterror:[4,10],iss:4,issu:[0,4,10],its:[4,10],job:[3,7],json:4,jti:4,jwt:[1,2,4,9,10],jzozkrta8b:4,kei:[2,4],kid:4,killmail:4,kind:1,known:[4,10],kwarg:4,last_valu:10,latest:4,layer:5,lazili:[4,10],lazyreferencefield:[4,10],lead:[4,10],least:10,level:2,levelnam:2,librari:[4,10],like:[1,4,10],line:[8,9],list:[0,4,5,10],listfield:[4,10],load:[2,4],load_configuration_fil:2,load_esi_openapi:4,locat:[2,4,9],log:[1,2,10],logger:2,login:4,login_url:0,look:[1,4],lqjg2:4,magic:3,mail:4,main:[4,5],maintain:[9,10],mainten:10,make:[3,4],manag:[0,4,7,10],manage_planet:4,mani:[4,10],manual:[1,10],mapfield:[4,10],market:4,match:5,mean:[4,10],member:[7,10],messag:2,metadata:[4,10],method:[4,10],microsecond:[4,10],migrat:3,migrate_ensure_root:3,migrate_ensure_root_dyn_token:3,migrate_ensure_root_per_token:3,migrate_ensure_superuser_group:3,millisecond:[4,10],min:10,mode:2,model:[0,1,4,10],modifi:[4,10],mongo:5,mongo_initdb_root_password:5,mongo_initdb_root_usernam:5,mongodb:[2,3,4,5,10],mongoengin:[0,3,4,10],more:4,multipl:[4,9,10],multipleobjectsreturn:[4,10],must:[0,1,4,10],mutablemap:2,my3rdpartyclientid:4,name:[2,4,10],namespac:8,nearest:[4,10],necessari:[4,10],need:[4,10],nested_dict:2,net:4,none:[0,2,3,4,8,10],note:[1,4,10],notif:[0,1],notifi:0,now:[9,10],nullifi:[4,10],oauth:[0,4],object:[4,10],objectid:[4,10],obtain:1,on_behalf_of:0,onc:[0,1],one:[4,10],onli:[4,10],open_window:4,openapi:[0,4,5],openssl:2,option:[0,4,10],order:1,org:[4,10],organize_mail:4,origin:[5,9],other:[0,10],otherwis:10,own:[3,10],owner:[0,3,4,10],owner_character_id:0,page:5,param:0,paramet:4,parent:[0,10],parent_kei:2,pars:[4,8,10],parse_command_line_argu:8,parser:[4,10],part:10,pass:[4,10],password:[2,5],path:[0,2,4],path_r:4,pdt:0,penalti:10,per:[0,10],perform:[4,10],perman:[0,1,3,10],permission_error_handl:0,permissionerror:[0,10],planet:4,point:8,pong:0,poor:[4,10],port:2,portal:[2,5],post:[0,4],post_token_dyn:0,post_token_p:0,post_token_use_from_dyn:0,post_token_use_from_p:0,postcallbackesiout:[0,1],posttokendynin:0,posttokendynout:0,posttokenperin:0,posttokenperout:0,posttokenusefromdynin:0,posttokenusefromdynout:[0,1],postusefromperout:[0,1],pre:[4,10],precis:[4,10],predefin:0,prepres:10,present:[4,10],prevent:[4,10],print:0,print_openapi_spec:0,priviledg:10,privileg:1,probabl:[4,10],prone:[9,10],propag:2,properti:[4,10],provid:10,publicdata:4,pull:[4,10],pumba:5,put:4,pwd:5,pydant:[0,4],pyjwt:2,python:[4,10],python_main_modul:5,queryset:[4,10],rais:[2,4,10],rand:2,read:[4,10],read_agents_research:4,read_asset:4,read_blueprint:4,read_calendar_ev:4,read_character_bookmark:4,read_character_contract:4,read_character_job:4,read_character_min:4,read_character_ord:4,read_character_wallet:4,read_chat_channel:4,read_clon:4,read_contact:4,read_container_log:4,read_corporation_asset:4,read_corporation_bookmark:4,read_corporation_contract:4,read_corporation_job:4,read_corporation_killmail:4,read_corporation_membership:4,read_corporation_min:4,read_corporation_ord:4,read_corporation_rol:4,read_corporation_wallet:4,read_customs_offic:4,read_divis:4,read_facil:4,read_fatigu:4,read_fit:4,read_fleet:4,read_fw_stat:4,read_impl:4,read_killmail:4,read_loc:4,read_loyalti:4,read_mail:4,read_med:4,read_notif:4,read_onlin:4,read_opportun:4,read_ship_typ:4,read_skil:4,read_skillqueu:4,read_stand:4,read_starbas:4,read_structur:4,read_titl:4,readwrit:5,receiv:0,redi:[2,5],refer:[0,3,4,5,10],referenc:[4,10],referencefield:[4,10],refresh:4,refresh_access_token:4,refresh_token:4,regard:10,regis:10,regist:[4,5,10],register_delete_rul:[4,10],relat:[0,10],relev:[4,10],remeb:10,repons:[0,4],repres:[4,10],request:[0,1,5],requir:[1,4,5,10],required_clear:10,respond_calendar_ev:4,respons:[0,1,4],result:10,retriev:[4,10],reverse_delete_rul:[4,10],revok:1,rguc:4,right:[9,10],role:5,root:[1,2,3,5,10],root_url:2,rootpassword:5,round:[4,10],router:[1,5],rule:[4,10],run:[3,8],safer:[9,10],same:[4,10],save:4,save_esi_token:4,schedul:5,scheduler_process_count:2,scope:[0,5,9,10],scope_level:10,scp:4,search:[4,5],search_structur:4,second:[4,10],secret:2,secretsecretsecretsecretsecretsecret0000:2,secretsecretsecretsecretsecretsecretsecretsecretsecretsecret0000:2,see:[1,2,4,5,10],send_mail:4,sent:1,separ:2,server:[2,5,8],servic:5,set:[2,4,10],set_clearance_level_x:10,shell:5,should:[1,3,4,10],signatur:4,simpli:[7,10],singl:10,skill:4,sni:[1,2,3,7,8,9],snipassword:[2,5],solv:[4,10],some:[4,10],sourc:[0,2,3,4,8,10],specif:[0,4,5,10],src:5,sso:[0,1,9,10],stage:4,standard:[2,4,10],start:10,start_api_serv:8,state:[0,4,10],state_cod:[0,1],statecod:10,status_cod:0,stdout:2,str:[0,2,4,10],stream:2,streamhandl:2,string:[4,10],strptime:[4,10],structure_market:4,sub:4,subsequ:1,suffici:10,suitabl:4,superus:[3,10],support:[2,4,9,10],sure:3,swagger:[4,6],syntax:[4,10],sys:2,take:1,target:10,task:10,tell:10,thei:10,them:0,themselv:1,thi:[1,4,8,10],ticker:10,tied:[0,1],time:[4,10],to_jwt:10,todo:5,token:[1,3,9],token_str:10,token_typ:[0,4,10],tokentyp:[0,10],too:[9,10],trace:0,track_memb:4,two:[1,10],type:[4,10],uac:[0,5,9],under:1,unicod:[4,10],univers:4,updat:[4,10],updated_on:[4,10],url:[0,2,4,10],urlsafe_b64encod:4,use:[0,1,4,5,7,10],used:[0,4,10],useful:[4,10],user1:10,user2:10,user:[0,1,3,4,5,9],user_token:[0,1],usernam:[2,5],using:[0,4,10],usr:5,utc:[4,10],utcnow:[4,10],utilis:[4,10],uuid:[0,10],valid:[1,4,9,10],validate_head:[0,10],valu:[2,4,10],vari:[4,10],variou:[3,10],verif:10,version:[2,4,5,10],via:1,volum:5,wai:[4,5,10],wallet:4,warn:10,web:[0,4],web_based_sso_flow:4,wether:10,what:[4,10],when:[0,4,9,10],where:10,which:[0,1,2,4,10],wish:1,workspac:9,wrap:[4,10],wrapper:[4,10],write:10,write_contact:4,write_fit:4,write_fleet:4,write_waypoint:4,yaml:[0,2,6],yml:[2,5],you:[4,10],your:5},titles:["API Server","Authentication","Configuration facility","Database layer","ESI requests layer","SeAT Navy Issue","OpenAPI specification","Scheduler","Main module","Todo list","User Access Control"],titleterms:{access:10,api:0,authent:1,clearanc:10,configur:2,control:10,databas:3,document:[2,4,5,10],esi:[0,4],etc:10,exampl:2,facil:2,group:10,high:5,indic:5,issu:5,layer:[3,4],level:[5,10],list:9,main:[0,8],modul:[0,2,4,5,8,10],navi:5,openapi:6,refer:2,request:4,router:0,run:5,schedul:7,scope:4,seat:5,server:0,sni:[0,4,5,10],specif:6,sso:4,tabl:5,todo:[4,9,10],token:[0,4,10],uac:10,user:10}})