Search.setIndex({docnames:["apiserver","authentication","configuration","database","esi","index","openapi","sni","todos","uac"],envversion:{"sphinx.domains.c":1,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":1,"sphinx.domains.index":1,"sphinx.domains.javascript":1,"sphinx.domains.math":2,"sphinx.domains.python":1,"sphinx.domains.rst":1,"sphinx.domains.std":1,"sphinx.ext.todo":2,"sphinx.ext.viewcode":1,sphinx:56},filenames:["apiserver.rst","authentication.rst","configuration.rst","database.rst","esi.rst","index.rst","openapi.rst","sni.rst","todos.rst","uac.rst"],objects:{"sni.conf":{assert_is_set:[2,1,1,""],flatten_dict:[2,1,1,""],get:[2,1,1,""],load_configuration_file:[2,1,1,""]},"sni.db":{init:[3,1,1,""],migrate:[3,1,1,""],migrate_ensure_root:[3,1,1,""],migrate_ensure_root_dyn_token:[3,1,1,""],migrate_ensure_root_per_token:[3,1,1,""],migrate_ensure_superuser_group:[3,1,1,""]},"sni.esi":{esi:[4,0,0,"-"],sso:[4,0,0,"-"],token:[4,0,0,"-"]},"sni.esi.esi":{"delete":[4,1,1,""],EsiPath:[4,2,1,""],get:[4,1,1,""],get_path_scope:[4,1,1,""],load_esi_openapi:[4,1,1,""],post:[4,1,1,""],put:[4,1,1,""],request:[4,1,1,""]},"sni.esi.esi.EsiPath":{DoesNotExist:[4,3,1,""],MultipleObjectsReturned:[4,3,1,""],http_method:[4,4,1,""],id:[4,4,1,""],objects:[4,4,1,""],path:[4,4,1,""],path_re:[4,4,1,""],scope:[4,4,1,""],version:[4,4,1,""]},"sni.esi.sso":{AuthorizationCodeResponse:[4,2,1,""],DecodedAccessToken:[4,2,1,""],decode_access_token:[4,1,1,""],get_access_token:[4,1,1,""],get_auth_url:[4,1,1,""],get_basic_authorization_code:[4,1,1,""],refresh_access_token:[4,1,1,""]},"sni.esi.sso.AuthorizationCodeResponse":{access_token:[4,4,1,""],expires_in:[4,4,1,""],refresh_token:[4,4,1,""],token_type:[4,4,1,""]},"sni.esi.sso.DecodedAccessToken":{azp:[4,4,1,""],character_id:[4,5,1,""],exp:[4,4,1,""],iss:[4,4,1,""],jti:[4,4,1,""],kid:[4,4,1,""],name:[4,4,1,""],owner:[4,4,1,""],scp:[4,4,1,""],sub:[4,4,1,""]},"sni.esi.token":{EsiAccessToken:[4,2,1,""],EsiRefreshToken:[4,2,1,""],get_access_token:[4,1,1,""],save_esi_tokens:[4,1,1,""]},"sni.esi.token.EsiAccessToken":{DoesNotExist:[4,3,1,""],MultipleObjectsReturned:[4,3,1,""],access_token:[4,4,1,""],created_on:[4,4,1,""],expires_on:[4,4,1,""],id:[4,4,1,""],objects:[4,4,1,""],owner:[4,4,1,""],scopes:[4,4,1,""]},"sni.esi.token.EsiRefreshToken":{DoesNotExist:[4,3,1,""],MultipleObjectsReturned:[4,3,1,""],created_on:[4,4,1,""],id:[4,4,1,""],objects:[4,4,1,""],owner:[4,4,1,""],refresh_token:[4,4,1,""],scopes:[4,4,1,""],updated_on:[4,4,1,""]},"sni.routers":{esi:[0,0,0,"-"],token:[0,0,0,"-"]},"sni.routers.esi":{EsiRequestIn:[0,2,1,""],EsiRequestOut:[0,2,1,""],PostCallbackEsiOut:[0,2,1,""],get_callback_esi:[0,1,1,""],get_esi_latest:[0,1,1,""]},"sni.routers.esi.EsiRequestIn":{on_behalf_of:[0,4,1,""],params:[0,4,1,""]},"sni.routers.esi.EsiRequestOut":{data:[0,4,1,""],headers:[0,4,1,""],status_code:[0,4,1,""]},"sni.routers.esi.PostCallbackEsiOut":{state_code:[0,4,1,""],user_token:[0,4,1,""]},"sni.routers.token":{GetTokenOut:[0,2,1,""],PostTokenDynIn:[0,2,1,""],PostTokenDynOut:[0,2,1,""],PostTokenPerIn:[0,2,1,""],PostTokenPerOut:[0,2,1,""],PostTokenUseFromDynIn:[0,2,1,""],PostTokenUseFromDynOut:[0,2,1,""],PostUseFromPerOut:[0,2,1,""],delete_token:[0,1,1,""],get_token:[0,1,1,""],post_token_dyn:[0,1,1,""],post_token_per:[0,1,1,""],post_token_use_from_dyn:[0,1,1,""],post_token_use_from_per:[0,1,1,""]},"sni.routers.token.GetTokenOut":{callback:[0,4,1,""],comments:[0,4,1,""],created_on:[0,4,1,""],expires_on:[0,4,1,""],owner_character_id:[0,4,1,""],parent:[0,4,1,""],token_type:[0,4,1,""],uuid:[0,4,1,""]},"sni.routers.token.PostTokenDynIn":{callback:[0,4,1,""],comments:[0,4,1,""]},"sni.routers.token.PostTokenDynOut":{app_token:[0,4,1,""]},"sni.routers.token.PostTokenPerIn":{callback:[0,4,1,""],comments:[0,4,1,""]},"sni.routers.token.PostTokenPerOut":{app_token:[0,4,1,""]},"sni.routers.token.PostTokenUseFromDynIn":{scopes:[0,4,1,""]},"sni.routers.token.PostTokenUseFromDynOut":{login_url:[0,4,1,""],state_code:[0,4,1,""]},"sni.routers.token.PostUseFromPerOut":{user_token:[0,4,1,""]},"sni.uac":{token:[9,0,0,"-"],user:[9,0,0,"-"]},"sni.uac.token":{StateCode:[9,2,1,""],Token:[9,2,1,""],create_dynamic_app_token:[9,1,1,""],create_permanent_app_token:[9,1,1,""],create_state_code:[9,1,1,""],create_user_token:[9,1,1,""],get_token_from_jwt:[9,1,1,""],to_jwt:[9,1,1,""],validate_header:[9,1,1,""]},"sni.uac.token.StateCode":{DoesNotExist:[9,3,1,""],MultipleObjectsReturned:[9,3,1,""],app_token:[9,4,1,""],created_on:[9,4,1,""],id:[9,4,1,""],objects:[9,4,1,""],uuid:[9,4,1,""]},"sni.uac.token.Token":{DoesNotExist:[9,3,1,""],MultipleObjectsReturned:[9,3,1,""],TokenType:[9,2,1,""],callback:[9,4,1,""],comments:[9,4,1,""],created_on:[9,4,1,""],expires_on:[9,4,1,""],id:[9,4,1,""],objects:[9,4,1,""],owner:[9,4,1,""],parent:[9,4,1,""],token_type:[9,4,1,""],uuid:[9,4,1,""]},"sni.uac.token.Token.TokenType":{_generate_next_value_:[9,5,1,""],_member_map_:[9,4,1,""],_member_names_:[9,4,1,""],_member_type_:[9,4,1,""],_value2member_map_:[9,4,1,""],dyn:[9,4,1,""],per:[9,4,1,""],use:[9,4,1,""]},"sni.uac.user":{Group:[9,2,1,""],User:[9,2,1,""],create_group:[9,1,1,""],get_user:[9,1,1,""]},"sni.uac.user.Group":{DoesNotExist:[9,3,1,""],MultipleObjectsReturned:[9,3,1,""],created_on:[9,4,1,""],description:[9,4,1,""],id:[9,4,1,""],members:[9,4,1,""],name:[9,4,1,""],objects:[9,4,1,""],owner:[9,4,1,""],updated_on:[9,4,1,""]},"sni.uac.user.User":{DoesNotExist:[9,3,1,""],MultipleObjectsReturned:[9,3,1,""],character_id:[9,4,1,""],character_name:[9,4,1,""],created_on:[9,4,1,""],id:[9,4,1,""],objects:[9,4,1,""],subcharacter_ids:[9,4,1,""]},sni:{conf:[2,0,0,"-"],db:[3,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","function","Python function"],"2":["py","class","Python class"],"3":["py","exception","Python exception"],"4":["py","attribute","Python attribute"],"5":["py","method","Python method"]},objtypes:{"0":"py:module","1":"py:function","2":"py:class","3":"py:exception","4":"py:attribute","5":"py:method"},terms:{"24h":1,"2c48822e0a1b":4,"43c5":4,"478b":1,"48h":1,"4df0":1,"8pmzcetkb4vfudrhlc":4,"998e12c7":4,"byte":9,"class":[0,2,4,9],"default":[2,4,9],"enum":9,"function":[4,9],"int":[0,4,9],"new":[0,4,9],"null":[4,9],"public":4,"return":[0,3,4,9],"short":[4,9],"true":2,"try":[4,9],"while":9,EVE:[0,2,4,5,9],For:9,The:[1,2,4,5,8,9],Then:5,There:1,Use:[4,9],Uses:[4,9],_cl:[4,9],_generate_next_value_:9,_member_map_:9,_member_names_:9,_member_type_:9,_value2member_map_:9,a8b9:1,about:[0,9],abov:9,accept:[4,9],access:[4,5],access_token:4,accur:[4,9],act:3,action:9,actor:9,actual:9,add:[4,9],added:[4,9],admin:2,aezxdswm:4,affili:5,after:[1,3],against:9,algorithm:2,alia:9,all:[1,5,9],allianc:[4,9],allow:[4,9],along:4,alreadi:[4,9],also:[1,2],altari:5,altern:[4,9],ani:[0,2,3,4,9],anyhttpurl:0,anyth:[3,4,9],api:[1,2,4,5,9],apimodel:0,app:[0,1,2,3,5,9],app_token:[0,9],applic:[0,1,2,4,5],arg:[4,9],argument:[4,9],around:[4,9],arrai:9,asctim:2,assert_is_set:2,asset:[4,9],associ:[4,9],async:0,authent:[0,5,9],authentication_sourc:2,author:[1,4,9],authorizationcoderespons:4,automat:[4,9],avail:[4,9],azp:4,baee74e2d517:1,base:[0,4,9],basemodel:[0,4],bash:5,bearer:[1,4,9],becaus:[4,9],befor:[4,9],being:0,bit:9,bloke:4,bookmark:4,broken:[4,9],builtin:9,c_a:2,c_b_x:2,c_b_y:2,calendar:4,call:[0,3,4],callback:[0,5,9],can:[0,1,4,9],cannot:[4,9],cascad:[4,9],certain:9,chang:[4,5,9],charact:[4,9],character_id:[1,4,9],character_nam:9,characterstat:4,check:9,chr:9,client_id:[2,4],client_secret:[2,4],clone:4,coa:9,coalit:9,code:[0,4,5,9],collect:9,com:[2,4,5],comment:[0,9],commun:4,complexdatetimefield:[4,9],compos:5,compris:9,conf:2,config:2,configur:5,connect:3,consid:[4,9],contain:[4,5,9],container_nam:5,contract:4,control:5,convert:[4,9],corpor:[4,9],correspond:9,count:9,creat:[0,2,3,4,5,9],create_dynamic_app_token:9,create_group:9,create_permanent_app_token:9,create_state_cod:9,create_user_token:9,created_on:[0,4,9],createus:5,credit:2,crp:9,current:[0,4,9],custom:[4,9],data:[0,5],databas:[2,4,5,9],date:[4,9],datetim:[0,4,9],datetimefield:[4,9],dateutil:[4,9],dcbd81af:1,debug:2,decod:4,decode_access_token:4,decodedaccesstoken:4,delet:[0,4,9],delete_token:0,deni:[4,9],depend:[0,4,9],derefer:[4,9],dereferenc:[4,9],deriv:[1,4,9],descript:9,develop:[2,5],dict:[0,2],dictfield:[4,9],dictionnari:2,direct:[4,9],disable_existing_logg:2,do_noth:[4,9],doc:4,docker:5,docstr:8,document:[0,3],doe:[2,3,4,9],doesnotexist:[4,9],domain:5,don:[4,5,9],done:[0,1],dyn:[0,9],dynam:[0,1,3,9],easiest:5,editor:6,effect:[4,9],either:9,embeddeddocu:[4,9],empti:[4,9],end:9,endpoint:9,entiti:9,entri:8,enumer:9,environ:5,error:[4,9],esi:[1,2,5,8,9],esi_path:0,esi_respons:4,esi_scop:4,esiaccesstoken:4,esipath:4,esirefreshtoken:4,esirequestin:0,esirequestout:0,especi:[4,9],etc:5,eveonlin:4,everytim:[4,9],evetech:4,exampl:[4,5,9],except:[2,4,9],exec:5,exist:[3,9],exp:4,expir:1,expires_in:4,expires_on:[0,4,9],ext:2,extend:[4,9],extra:[4,9],extract:4,eyjhbgcioijiuzi1niisin:1,facil:5,fals:2,fastapi:9,featur:[4,9],fetch:9,field:[4,9],file:[2,5,6],first:[4,9],fit:4,flatten:2,flatten_dict:2,fleet:4,follow:[5,9],forget:5,form:[1,4],format:[2,4,9],formatt:2,forward:0,found:4,from:[0,1,2,4,9],fulli:[4,9],gener:2,get:[0,1,2,4,9],get_access_token:[4,8],get_auth_url:4,get_basic_authorization_cod:4,get_callback_esi:0,get_esi_latest:0,get_path_scop:4,get_token:0,get_token_from_jwt:9,get_us:9,gettokenout:0,git:5,git_url:5,github:[5,8],given:[4,9],group:[3,5],grp:9,handl:[4,9],handler:2,happen:[4,9],have:[2,6],header:[0,1,9],here:[2,6],hex:2,host:2,hs256:2,html:4,http:[2,4,5],http_method:4,idididididididididididididididid:2,imag:5,immedi:3,implement:[4,9],imran:2,inact:1,includ:1,index:5,industri:4,info:2,inform:0,inherit:1,init:3,initi:[3,4],input:9,instal:[4,9],instanc:[3,4,9],integ:9,interfac:4,invaliddocumenterror:[4,9],iss:4,issu:[0,4,9],its:[4,9],job:3,json:4,jti:4,jwt:[1,2,4,8,9],jzozkrta8b:4,kei:[2,4],kid:4,killmail:4,kind:1,known:[4,9],kwarg:4,last_valu:9,latest:4,layer:5,lazili:[4,9],lazyreferencefield:[4,9],lead:[4,9],level:2,levelnam:2,librari:[4,9],like:[1,4],line:8,list:[0,4,5,9],listfield:[4,9],load:[2,4],load_configuration_fil:2,load_esi_openapi:4,locat:[2,4,8],log:[1,2,9],logger:2,login:4,login_url:0,look:[1,4],lqjg2:4,magic:3,mail:4,main:[4,5],make:[3,4],manag:[0,4,9],manage_planet:4,mani:[4,9],manual:1,mapfield:[4,9],market:4,match:5,mean:[4,9],member:9,messag:2,metadata:[4,9],method:[4,9],microsecond:[4,9],migrat:3,migrate_ensure_root:3,migrate_ensure_root_dyn_token:3,migrate_ensure_root_per_token:3,migrate_ensure_superuser_group:3,millisecond:[4,9],mode:2,model:[0,1,4,9],modifi:[4,9],mongo:5,mongo_initdb_root_password:5,mongo_initdb_root_usernam:5,mongodb:[2,3,4,5,9],mongoengin:[3,4,9],more:4,multipl:[4,8,9],multipleobjectsreturn:[4,9],must:[0,1,4,9],mutablemap:2,my3rdpartyclientid:4,name:[2,4,9],nearest:[4,9],necessari:[4,9],need:[4,9],nested_dict:2,net:4,none:[0,2,3,4,9],note:[1,4,9],notif:[0,1],notifi:0,nullifi:[4,9],oauth:[0,4],object:[4,9],objectid:[4,9],obtain:1,on_behalf_of:0,onc:[0,1],one:[4,9],onli:[4,9],open_window:4,openapi:[4,5],openssl:2,option:[0,4,9],order:1,org:[4,9],organize_mail:4,origin:[5,8],other:9,own:3,owner:[0,3,4,9],owner_character_id:0,page:5,param:0,paramet:4,parent:[0,9],parent_kei:2,pars:[4,9],parser:[4,9],pass:[4,9],password:[2,5],path:[0,2,4],path_r:4,pdt:0,per:[0,9],perform:[4,9],perman:[0,1,3,9],planet:4,poor:[4,9],port:2,portal:[2,5],post:[0,4],post_token_dyn:0,post_token_p:0,post_token_use_from_dyn:0,post_token_use_from_p:0,postcallbackesiout:[0,1],posttokendynin:0,posttokendynout:0,posttokenperin:0,posttokenperout:0,posttokenusefromdynin:0,posttokenusefromdynout:[0,1],postusefromperout:[0,1],pre:[4,9],precis:[4,9],predefin:0,present:[4,9],prevent:[4,9],privileg:1,probabl:[4,9],propag:2,properti:4,proxi:9,publicdata:4,pull:[4,9],pumba:5,put:4,pwd:5,pydant:[0,4],pyjwt:2,python:[4,9],python_main_modul:5,queryset:[4,9],rais:[2,4,9],rand:2,read:4,read_agents_research:4,read_asset:4,read_blueprint:4,read_calendar_ev:4,read_character_bookmark:4,read_character_contract:4,read_character_job:4,read_character_min:4,read_character_ord:4,read_character_wallet:4,read_chat_channel:4,read_clon:4,read_contact:4,read_container_log:4,read_corporation_asset:4,read_corporation_bookmark:4,read_corporation_contract:4,read_corporation_job:4,read_corporation_killmail:4,read_corporation_membership:4,read_corporation_min:4,read_corporation_ord:4,read_corporation_rol:4,read_corporation_wallet:4,read_customs_offic:4,read_divis:4,read_facil:4,read_fatigu:4,read_fit:4,read_fleet:4,read_fw_stat:4,read_impl:4,read_killmail:4,read_loc:4,read_loyalti:4,read_mail:4,read_med:4,read_notif:4,read_onlin:4,read_opportun:4,read_ship_typ:4,read_skil:4,read_skillqueu:4,read_stand:4,read_starbas:4,read_structur:4,read_titl:4,readwrit:5,receiv:0,redi:[2,5],refer:[0,3,4,5,9],referenc:[4,9],referencefield:[4,9],refresh:4,refresh_access_token:4,refresh_token:4,regist:[4,5,9],register_delete_rul:[4,9],relat:[0,9],relev:[4,9],remeb:9,repons:[0,4],repres:[4,9],request:[0,1,5,9],requir:[1,4,5,9],respond_calendar_ev:4,respons:[0,1,4],retriev:[4,9],reverse_delete_rul:[4,9],revok:1,rguc:4,role:5,root:[1,2,3,5],root_url:2,rootpassword:5,round:[4,9],router:[1,5],rule:[4,9],run:3,same:[4,9],save:4,save_esi_token:4,scope:[0,5,8,9],scp:4,search:[4,5],search_structur:4,second:[4,9],secret:2,secretsecretsecretsecretsecretsecret0000:2,secretsecretsecretsecretsecretsecretsecretsecretsecretsecret0000:2,see:[1,2,4,5,9],send_mail:4,sent:1,separ:[2,9],server:[2,5],servic:5,set:[2,4,9],shell:5,should:[1,3,4,9],signatur:4,simpli:9,singl:9,skill:4,sni:[1,2,3,8],snipassword:[2,5],solv:[4,9],some:[4,9],sourc:[0,2,3,4,9],specif:[4,5],src:5,sso:[0,1,8,9],stage:4,standard:[2,4,9],start:9,state:[0,4,9],state_cod:[0,1],statecod:9,status_cod:0,stdout:2,store:9,str:[0,2,4,9],stream:2,streamhandl:2,string:[4,9],strptime:[4,9],structure_market:4,sub:[4,9],subcharacter_id:9,subsequ:1,suitabl:4,superus:3,support:[2,4,8,9],sure:3,swagger:[4,6],syntax:[4,9],sys:2,tabl:9,take:1,themselv:1,thi:[1,4,9],tied:[0,1],time:[4,9],to_jwt:9,todo:5,token:[1,3,8],token_str:9,token_typ:[0,4,9],tokentyp:[0,9],track_memb:4,tupl:9,two:1,type:[4,9],uac:[0,5],under:1,unicod:[4,9],univers:4,updat:[4,9],updated_on:[4,9],url:[0,2,4,9],urlsafe_b64encod:4,use:[0,1,4,5,9],used:[0,4,9],useful:[4,9],user:[0,1,3,4,5],user_token:[0,1],usernam:[2,5],using:[0,4,9],usr:5,utc:[4,9],utcnow:[4,9],utilis:[4,9],uuid:[0,9],valid:[1,4,8,9],validate_head:[0,9],valu:[2,4,9],vari:[4,9],variou:[3,9],version:[2,4,5,9],via:1,volum:5,wai:[4,5,9],wallet:4,warn:9,web:[0,4],web_based_sso_flow:4,well:9,what:[4,9],when:[0,4,9],where:9,which:[0,1,2,4,9],whose:9,wish:[1,9],within:9,workspac:8,wrap:[4,9],wrapper:[4,9],write_contact:4,write_fit:4,write_fleet:4,write_waypoint:4,yaml:[2,6],yml:[2,5],you:[4,9],your:5},titles:["API Server","Authentication","Configuration facility","Database layer","ESI requests layer","SeAT Navy Issue","OpenAPI specification","Main module","Todo list","User Access Control"],titleterms:{access:9,api:0,authent:1,configur:2,control:9,databas:3,document:[2,4,5,9],esi:[0,4],etc:9,exampl:2,facil:2,group:9,high:5,indic:5,issu:5,layer:[3,4],level:5,list:8,main:[0,7],modul:[0,2,4,5,7,9],navi:5,openapi:6,refer:2,request:4,router:0,run:5,scope:4,seat:5,server:0,sni:[0,4,5,9],specif:6,sso:4,tabl:5,todo:[4,8],token:[0,4,9],uac:9,user:9}})