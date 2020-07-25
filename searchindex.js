Search.setIndex({docnames:["api","authentication","command-line-arguments","configuration","db","discord","esi","index","indexation","openapi","sde","sni","teamspeak","todos","uac","user"],envversion:{"sphinx.domains.c":1,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":1,"sphinx.domains.index":1,"sphinx.domains.javascript":1,"sphinx.domains.math":2,"sphinx.domains.python":1,"sphinx.domains.rst":1,"sphinx.domains.std":1,"sphinx.ext.todo":2,"sphinx.ext.viewcode":1,sphinx:56},filenames:["api.rst","authentication.rst","command-line-arguments.rst","configuration.rst","db.rst","discord.rst","esi.rst","index.rst","indexation.rst","openapi.rst","sde.rst","sni.rst","teamspeak.rst","todos.rst","uac.rst","user.rst"],objects:{"sni.__main__":{configure_logging:[11,1,1,""],connect_database_signals:[11,1,1,""],main:[11,1,1,""],migrate_database:[11,1,1,""],parse_command_line_arguments:[11,1,1,""],schedule_jobs:[11,1,1,""],start_discord_bot:[11,1,1,""]},"sni.api":{jobs:[0,0,0,"-"],migration:[0,0,0,"-"],models:[0,0,0,"-"],server:[0,0,0,"-"],signals:[0,0,0,"-"]},"sni.api.migration":{migrate:[0,1,1,""]},"sni.api.models":{CrashReport:[0,2,1,""],CrashReportRequest:[0,2,1,""],CrashReportToken:[0,2,1,""]},"sni.api.models.CrashReport":{SCHEMA_VERSION:[0,3,1,""],_version:[0,3,1,""],request:[0,3,1,""],timestamp:[0,3,1,""],to_dict:[0,4,1,""],token:[0,3,1,""],trace:[0,3,1,""]},"sni.api.models.CrashReportRequest":{headers:[0,3,1,""],method:[0,3,1,""],params:[0,3,1,""],to_dict:[0,4,1,""],url:[0,3,1,""]},"sni.api.models.CrashReportToken":{created_on:[0,3,1,""],expires_on:[0,3,1,""],owner:[0,3,1,""],to_dict:[0,4,1,""],token_type:[0,3,1,""],uuid:[0,3,1,""]},"sni.api.routers":{alliance:[0,0,0,"-"],callback:[0,0,0,"-"],coalition:[0,0,0,"-"],corporation:[0,0,0,"-"],esi:[0,0,0,"-"],group:[0,0,0,"-"],system:[0,0,0,"-"],teamspeak:[0,0,0,"-"],token:[0,0,0,"-"],user:[0,0,0,"-"]},"sni.api.routers.alliance":{get_alliance_tracking:[0,1,1,""],post_alliance:[0,1,1,""]},"sni.api.routers.callback":{get_callback_esi:[0,1,1,""]},"sni.api.routers.coalition":{GetCoalitionOut:[0,2,1,""],GetCoalitionShortOut:[0,2,1,""],PostCoalitionIn:[0,2,1,""],PutCoalitionIn:[0,2,1,""],delete_coalition:[0,1,1,""],get_coalition:[0,1,1,""],get_coalition_name:[0,1,1,""],get_coalition_tracking:[0,1,1,""],post_coalitions:[0,1,1,""],put_coalition:[0,1,1,""]},"sni.api.routers.coalition.GetCoalitionOut":{authorized_to_login:[0,3,1,""],coalition_id:[0,3,1,""],coalition_name:[0,3,1,""],created_on:[0,3,1,""],from_record:[0,4,1,""],mandatory_esi_scopes:[0,3,1,""],members:[0,3,1,""],ticker:[0,3,1,""],updated_on:[0,3,1,""]},"sni.api.routers.coalition.GetCoalitionShortOut":{coalition_id:[0,3,1,""],coalition_name:[0,3,1,""],from_record:[0,4,1,""]},"sni.api.routers.coalition.PostCoalitionIn":{coalition_name:[0,3,1,""],ticker:[0,3,1,""]},"sni.api.routers.coalition.PutCoalitionIn":{add_members:[0,3,1,""],authorized_to_login:[0,3,1,""],mandatory_esi_scopes:[0,3,1,""],members:[0,3,1,""],remove_members:[0,3,1,""],ticker:[0,3,1,""]},"sni.api.routers.corporation":{GetTrackingOut:[0,2,1,""],get_corporation_tracking:[0,1,1,""],post_corporation:[0,1,1,""]},"sni.api.routers.corporation.GetTrackingOut":{from_user_iterator:[0,4,1,""],invalid_refresh_token:[0,3,1,""],no_refresh_token:[0,3,1,""],valid_refresh_token:[0,3,1,""]},"sni.api.routers.esi":{EsiRequestIn:[0,2,1,""],get_esi_latest:[0,1,1,""]},"sni.api.routers.esi.EsiRequestIn":{all_pages:[0,3,1,""],id_annotations:[0,3,1,""],on_behalf_of:[0,3,1,""],params:[0,3,1,""]},"sni.api.routers.group":{GetGroupOut:[0,2,1,""],GetGroupShortOut:[0,2,1,""],PostGroupIn:[0,2,1,""],PutGroupIn:[0,2,1,""],delete_group:[0,1,1,""],get_group:[0,1,1,""],get_group_name:[0,1,1,""],post_groups:[0,1,1,""],put_group:[0,1,1,""]},"sni.api.routers.group.GetGroupOut":{authorized_to_login:[0,3,1,""],created_on:[0,3,1,""],description:[0,3,1,""],from_record:[0,4,1,""],group_id:[0,3,1,""],group_name:[0,3,1,""],is_autogroup:[0,3,1,""],members:[0,3,1,""],owner:[0,3,1,""],updated_on:[0,3,1,""]},"sni.api.routers.group.GetGroupShortOut":{group_id:[0,3,1,""],group_name:[0,3,1,""]},"sni.api.routers.group.PostGroupIn":{description:[0,3,1,""],group_name:[0,3,1,""]},"sni.api.routers.group.PutGroupIn":{add_members:[0,3,1,""],authorized_to_login:[0,3,1,""],description:[0,3,1,""],members:[0,3,1,""],owner:[0,3,1,""],remove_members:[0,3,1,""]},"sni.api.routers.system":{GetJobOut:[0,2,1,""],get_jobs:[0,1,1,""],post_job:[0,1,1,""]},"sni.api.routers.system.GetJobOut":{"function":[0,3,1,""],coalesce:[0,3,1,""],executor:[0,3,1,""],from_job:[0,4,1,""],job_id:[0,3,1,""],max_instances:[0,3,1,""],misfire_grace_time:[0,3,1,""],name:[0,3,1,""],next_run_time:[0,3,1,""],trigger:[0,3,1,""]},"sni.api.routers.teamspeak":{PostAuthStartOut:[0,2,1,""],port_auth_start:[0,1,1,""],post_auth_complete:[0,1,1,""]},"sni.api.routers.teamspeak.PostAuthStartOut":{challenge_nickname:[0,3,1,""],expiration_datetime:[0,3,1,""],user:[0,3,1,""]},"sni.api.routers.token":{GetTokenOut:[0,2,1,""],PostTokenDynIn:[0,2,1,""],PostTokenDynOut:[0,2,1,""],PostTokenPerIn:[0,2,1,""],PostTokenPerOut:[0,2,1,""],PostTokenUseFromDynIn:[0,2,1,""],PostTokenUseFromDynOut:[0,2,1,""],PostUseFromPerOut:[0,2,1,""],delete_token:[0,1,1,""],get_token:[0,1,1,""],post_token_dyn:[0,1,1,""],post_token_per:[0,1,1,""],post_token_use_from_dyn:[0,1,1,""],post_token_use_from_per:[0,1,1,""]},"sni.api.routers.token.GetTokenOut":{callback:[0,3,1,""],comments:[0,3,1,""],created_on:[0,3,1,""],expires_on:[0,3,1,""],owner_character_id:[0,3,1,""],owner_character_name:[0,3,1,""],parent:[0,3,1,""],token_type:[0,3,1,""],uuid:[0,3,1,""]},"sni.api.routers.token.PostTokenDynIn":{callback:[0,3,1,""],comments:[0,3,1,""]},"sni.api.routers.token.PostTokenDynOut":{tkn:[0,3,1,""]},"sni.api.routers.token.PostTokenPerIn":{callback:[0,3,1,""],comments:[0,3,1,""]},"sni.api.routers.token.PostTokenPerOut":{tkn:[0,3,1,""]},"sni.api.routers.token.PostTokenUseFromDynIn":{scopes:[0,3,1,""]},"sni.api.routers.token.PostTokenUseFromDynOut":{login_url:[0,3,1,""],state_code:[0,3,1,""]},"sni.api.routers.token.PostUseFromPerOut":{user_token:[0,3,1,""]},"sni.api.routers.user":{GetUserOut:[0,2,1,""],GetUserShortOut:[0,2,1,""],PutUserIn:[0,2,1,""],delete_user:[0,1,1,""],get_user:[0,1,1,""],get_user_name:[0,1,1,""],put_user_name:[0,1,1,""]},"sni.api.routers.user.GetUserOut":{alliance:[0,3,1,""],authorized_to_login:[0,3,1,""],available_esi_scopes:[0,3,1,""],character_id:[0,3,1,""],character_name:[0,3,1,""],clearance_level:[0,3,1,""],coalitions:[0,3,1,""],corporation:[0,3,1,""],created_on:[0,3,1,""],cumulated_mandatory_esi_scopes:[0,3,1,""],from_record:[0,4,1,""],is_ceo_of_alliance:[0,3,1,""],is_ceo_of_corporation:[0,3,1,""],tickered_name:[0,3,1,""],updated_on:[0,3,1,""]},"sni.api.routers.user.GetUserShortOut":{character_id:[0,3,1,""],character_name:[0,3,1,""]},"sni.api.routers.user.PutUserIn":{authorized_to_login:[0,3,1,""],clearance_level:[0,3,1,""]},"sni.api.server":{get_ping:[0,1,1,""],print_openapi_spec:[0,1,1,""],start_api_server:[0,1,1,""]},"sni.conf":{assert_is_set:[11,1,1,""],flatten_dict:[11,1,1,""],get:[11,1,1,""],load_configuration_file:[11,1,1,""]},"sni.db":{migration:[4,0,0,"-"],mongodb:[4,0,0,"-"],redis:[4,0,0,"-"],signals:[4,0,0,"-"]},"sni.db.migration":{ensure_minimum_version:[4,1,1,""],has_outdated_documents:[4,1,1,""],set_if_not_exist:[4,1,1,""]},"sni.db.mongodb":{get_pymongo_collection:[4,1,1,""],init_mongodb:[4,1,1,""],new_pymongo_client:[4,1,1,""]},"sni.db.redis":{new_redis_connection:[4,1,1,""]},"sni.db.signals":{on_pre_save:[4,1,1,""]},"sni.discord":{bot:[5,0,0,"-"],commands:[5,0,0,"-"],discord:[5,0,0,"-"],events:[5,0,0,"-"],jobs:[5,0,0,"-"],migration:[5,0,0,"-"],signals:[5,0,0,"-"]},"sni.discord.bot":{JOBS_KEY:[5,5,1,""],RUN_TIMES_KEY:[5,5,1,""],get_guild:[5,1,1,""],get_member:[5,1,1,""],log:[5,1,1,""],start_bot:[5,1,1,""],start_scheduler:[5,1,1,""],stop_scheduler:[5,1,1,""]},"sni.discord.discord":{DiscordAuthenticationChallenge:[5,2,1,""],complete_authentication_challenge:[5,1,1,""],ensure_role_for_group:[5,1,1,""],new_authentication_challenge:[5,1,1,""]},"sni.discord.discord.DiscordAuthenticationChallenge":{code:[5,3,1,""],created_on:[5,3,1,""],user:[5,3,1,""]},"sni.discord.events":{on_disconnect:[5,1,1,""],on_ready:[5,1,1,""]},"sni.discord.jobs":{update_discord_role:[5,1,1,""],update_discord_roles:[5,1,1,""],update_discord_user:[5,1,1,""],update_discord_users:[5,1,1,""]},"sni.discord.migration":{migrate:[5,1,1,""]},"sni.esi":{esi:[6,0,0,"-"],jobs:[6,0,0,"-"],migration:[6,0,0,"-"],models:[6,0,0,"-"],signals:[6,0,0,"-"],sso:[6,0,0,"-"],token:[6,0,0,"-"]},"sni.esi.esi":{ESI_ANNOTATORS:[6,5,1,""],EsiResponse:[6,2,1,""],esi_delete:[6,1,1,""],esi_get:[6,1,1,""],esi_get_all_pages:[6,1,1,""],esi_post:[6,1,1,""],esi_put:[6,1,1,""],esi_request:[6,1,1,""],get_esi_path_scope:[6,1,1,""],id_annotations:[6,1,1,""],load_esi_openapi:[6,1,1,""]},"sni.esi.esi.EsiResponse":{data:[6,3,1,""],from_response:[6,4,1,""],headers:[6,3,1,""],id_annotations:[6,3,1,""],status_code:[6,3,1,""]},"sni.esi.jobs":{refresh_tokens:[6,1,1,""]},"sni.esi.migration":{migrate:[6,1,1,""],migrate_esi_access_token:[6,1,1,""],migrate_esi_refresh_token:[6,1,1,""]},"sni.esi.models":{EsiAccessToken:[6,2,1,""],EsiPath:[6,2,1,""],EsiRefreshToken:[6,2,1,""]},"sni.esi.models.EsiAccessToken":{SCHEMA_VERSION:[6,3,1,""],_version:[6,3,1,""],access_token:[6,3,1,""],created_on:[6,3,1,""],expires_on:[6,3,1,""],owner:[6,3,1,""],refresh_token:[6,3,1,""],scopes:[6,3,1,""]},"sni.esi.models.EsiPath":{http_method:[6,3,1,""],path:[6,3,1,""],path_re:[6,3,1,""],scope:[6,3,1,""],version:[6,3,1,""]},"sni.esi.models.EsiRefreshToken":{SCHEMA_VERSION:[6,3,1,""],_version:[6,3,1,""],created_on:[6,3,1,""],owner:[6,3,1,""],refresh_token:[6,3,1,""],scopes:[6,3,1,""],updated_on:[6,3,1,""],valid:[6,3,1,""]},"sni.esi.sso":{AuthorizationCodeResponse:[6,2,1,""],DecodedAccessToken:[6,2,1,""],EsiTokenError:[6,6,1,""],decode_access_token:[6,1,1,""],get_access_token_from_callback_code:[6,1,1,""],get_auth_url:[6,1,1,""],get_basic_authorization_code:[6,1,1,""],refresh_access_token:[6,1,1,""]},"sni.esi.sso.AuthorizationCodeResponse":{access_token:[6,3,1,""],expires_in:[6,3,1,""],refresh_token:[6,3,1,""],token_type:[6,3,1,""]},"sni.esi.sso.DecodedAccessToken":{azp:[6,3,1,""],character_id:[6,4,1,""],exp:[6,3,1,""],iss:[6,3,1,""],jti:[6,3,1,""],kid:[6,3,1,""],name:[6,3,1,""],owner:[6,3,1,""],scp:[6,3,1,""],sub:[6,3,1,""]},"sni.esi.token":{TrackingStatus:[6,2,1,""],available_esi_scopes:[6,1,1,""],esi_delete_on_befalf_of:[6,1,1,""],esi_get_on_befalf_of:[6,1,1,""],esi_post_on_befalf_of:[6,1,1,""],esi_put_on_befalf_of:[6,1,1,""],esi_request_on_behalf_of:[6,1,1,""],get_access_token:[6,1,1,""],has_esi_scope:[6,1,1,""],save_esi_tokens:[6,1,1,""],token_has_enough_scopes:[6,1,1,""],tracking_status:[6,1,1,""]},"sni.esi.token.TrackingStatus":{HAS_A_VALID_REFRESH_TOKEN:[6,3,1,""],HAS_NO_REFRESH_TOKEN:[6,3,1,""],ONLY_HAS_INVALID_REFRESH_TOKEN:[6,3,1,""]},"sni.index":{jobs:[8,0,0,"-"],migration:[8,0,0,"-"],models:[8,0,0,"-"],signals:[8,0,0,"-"]},"sni.index.jobs":{format_mail_body:[8,1,1,""],index_user_location:[8,1,1,""],index_user_mails:[8,1,1,""],index_user_skillpoints:[8,1,1,""],index_user_wallets:[8,1,1,""],index_users_location:[8,1,1,""],index_users_mails:[8,1,1,""],index_users_skillpoints:[8,1,1,""],index_users_wallets:[8,1,1,""]},"sni.index.migration":{migrate:[8,1,1,""]},"sni.index.models":{EsiCharacterLocation:[8,2,1,""],EsiMail:[8,2,1,""],EsiMailRecipient:[8,2,1,""],EsiSkillPoints:[8,2,1,""],EsiWalletBalance:[8,2,1,""]},"sni.index.models.EsiCharacterLocation":{online:[8,3,1,""],ship_item_id:[8,3,1,""],ship_name:[8,3,1,""],ship_type_id:[8,3,1,""],solar_system_id:[8,3,1,""],station_id:[8,3,1,""],structure_id:[8,3,1,""],timestamp:[8,3,1,""],user:[8,3,1,""]},"sni.index.models.EsiMail":{SCHEMA_VERSION:[8,3,1,""],_version:[8,3,1,""],body:[8,3,1,""],from_id:[8,3,1,""],mail_id:[8,3,1,""],recipients:[8,3,1,""],subject:[8,3,1,""],timestamp:[8,3,1,""]},"sni.index.models.EsiMailRecipient":{recipient_id:[8,3,1,""],recipient_type:[8,3,1,""]},"sni.index.models.EsiSkillPoints":{SCHEMA_VERSION:[8,3,1,""],_version:[8,3,1,""],timestamp:[8,3,1,""],total_sp:[8,3,1,""],unallocated_sp:[8,3,1,""],user:[8,3,1,""]},"sni.index.models.EsiWalletBalance":{balance:[8,3,1,""],timestamp:[8,3,1,""],user:[8,3,1,""]},"sni.scheduler":{JOBS_KEY:[11,5,1,""],RUN_TIMES_KEY:[11,5,1,""],_test_tick:[11,1,1,""],_test_tock:[11,1,1,""],run_scheduled:[11,1,1,""],start_scheduler:[11,1,1,""],stop_scheduler:[11,1,1,""]},"sni.sde":{jobs:[10,0,0,"-"],migration:[10,0,0,"-"],models:[10,0,0,"-"],sde:[10,0,0,"-"],signals:[10,0,0,"-"]},"sni.sde.jobs":{update_sde:[10,1,1,""]},"sni.sde.migration":{migrate:[10,1,1,""]},"sni.sde.models":{EsiObjectName:[10,2,1,""]},"sni.sde.models.EsiObjectName":{SCHEMA_VERSION:[10,3,1,""],_version:[10,3,1,""],expires_on:[10,3,1,""],field_id:[10,3,1,""],field_names:[10,3,1,""],name:[10,3,1,""]},"sni.sde.sde":{download_latest_sde:[10,1,1,""],get_latest_sde_md5:[10,1,1,""],import_sde_dump:[10,1,1,""],import_sde_dump_inv_categories:[10,1,1,""],import_sde_dump_inv_constellations:[10,1,1,""],import_sde_dump_inv_groups:[10,1,1,""],import_sde_dump_inv_solar_systems:[10,1,1,""],import_sde_dump_inv_types:[10,1,1,""],import_sde_dump_map_regions:[10,1,1,""],sde_get_name:[10,1,1,""]},"sni.teamspeak":{jobs:[12,0,0,"-"],migration:[12,0,0,"-"],models:[12,0,0,"-"],signals:[12,0,0,"-"],teamspeak:[12,0,0,"-"]},"sni.teamspeak.jobs":{map_teamspeak_groups:[12,1,1,""],message_registered_clients_with_wrong_name:[12,1,1,""],update_teamspeak_groups:[12,1,1,""]},"sni.teamspeak.migration":{migrate:[12,1,1,""]},"sni.teamspeak.models":{TeamspeakAuthenticationChallenge:[12,2,1,""]},"sni.teamspeak.models.TeamspeakAuthenticationChallenge":{challenge_nickname:[12,3,1,""],created_on:[12,3,1,""],user:[12,3,1,""]},"sni.teamspeak.teamspeak":{TeamspeakClient:[12,2,1,""],TeamspeakGroup:[12,2,1,""],cached_teamspeak_query:[12,1,1,""],client_list:[12,1,1,""],complete_authentication_challenge:[12,1,1,""],ensure_group:[12,1,1,""],find_client:[12,1,1,""],find_group:[12,1,1,""],group_list:[12,1,1,""],new_authentication_challenge:[12,1,1,""],new_teamspeak_connection:[12,1,1,""]},"sni.teamspeak.teamspeak.TeamspeakClient":{cid:[12,3,1,""],clid:[12,3,1,""],client_database_id:[12,3,1,""],client_nickname:[12,3,1,""],client_type:[12,3,1,""]},"sni.teamspeak.teamspeak.TeamspeakGroup":{iconid:[12,3,1,""],name:[12,3,1,""],savedb:[12,3,1,""],sgid:[12,3,1,""],type:[12,3,1,""]},"sni.uac":{clearance:[14,0,0,"-"],migration:[14,0,0,"-"],models:[14,0,0,"-"],signals:[14,0,0,"-"],token:[14,0,0,"-"],uac:[14,0,0,"-"]},"sni.uac.clearance":{AbsoluteScope:[14,2,1,""],AbstractScope:[14,2,1,""],ClearanceModificationScope:[14,2,1,""],ESIScope:[14,2,1,""],are_in_same_alliance:[14,1,1,""],are_in_same_coalition:[14,1,1,""],are_in_same_corporation:[14,1,1,""],assert_has_clearance:[14,1,1,""],distance_penalty:[14,1,1,""],has_clearance:[14,1,1,""],reset_clearance:[14,1,1,""]},"sni.uac.clearance.AbsoluteScope":{has_clearance:[14,4,1,""],level:[14,3,1,""]},"sni.uac.clearance.AbstractScope":{has_clearance:[14,4,1,""]},"sni.uac.clearance.ClearanceModificationScope":{has_clearance:[14,4,1,""],level:[14,3,1,""]},"sni.uac.clearance.ESIScope":{has_clearance:[14,4,1,""],level:[14,3,1,""]},"sni.uac.migration":{ensure_root_dyn_token:[14,1,1,""],ensure_root_per_token:[14,1,1,""],migrate:[14,1,1,""]},"sni.uac.models":{StateCode:[14,2,1,""],Token:[14,2,1,""]},"sni.uac.models.StateCode":{app_token:[14,3,1,""],created_on:[14,3,1,""],uuid:[14,3,1,""]},"sni.uac.models.Token":{TokenType:[14,2,1,""],callback:[14,3,1,""],comments:[14,3,1,""],created_on:[14,3,1,""],expires_on:[14,3,1,""],owner:[14,3,1,""],parent:[14,3,1,""],token_type:[14,3,1,""],uuid:[14,3,1,""]},"sni.uac.models.Token.TokenType":{dyn:[14,3,1,""],per:[14,3,1,""],use:[14,3,1,""]},"sni.uac.token":{create_dynamic_app_token:[14,1,1,""],create_permanent_app_token:[14,1,1,""],create_state_code:[14,1,1,""],create_user_token:[14,1,1,""],from_authotization_header:[14,1,1,""],from_authotization_header_nondyn:[14,1,1,""],get_token_from_jwt:[14,1,1,""],to_jwt:[14,1,1,""]},"sni.uac.uac":{is_authorized_to_login:[14,1,1,""]},"sni.user":{jobs:[15,0,0,"-"],migration:[15,0,0,"-"],models:[15,0,0,"-"],signals:[15,0,0,"-"],user:[15,0,0,"-"]},"sni.user.jobs":{ensure_alliance_members:[15,1,1,""],ensure_alliances_members:[15,1,1,""],ensure_corporation_members:[15,1,1,""],ensure_corporations_members:[15,1,1,""],update_alliance_autogroup:[15,1,1,""],update_alliance_autogroups:[15,1,1,""],update_alliance_from_esi:[15,1,1,""],update_alliances_from_esi:[15,1,1,""],update_coalition_autogroup:[15,1,1,""],update_coalition_autogroups:[15,1,1,""],update_corporation:[15,1,1,""],update_corporation_autogroup:[15,1,1,""],update_corporation_autogroups:[15,1,1,""],update_corporations:[15,1,1,""],update_user_autogroup:[15,1,1,""],update_user_from_esi:[15,1,1,""],update_users_from_esi:[15,1,1,""]},"sni.user.migration":{ensure_root:[15,1,1,""],ensure_superuser_group:[15,1,1,""],migrate:[15,1,1,""],migrate_alliance:[15,1,1,""],migrate_coalition:[15,1,1,""],migrate_corporation:[15,1,1,""],migrate_group:[15,1,1,""],migrate_user:[15,1,1,""]},"sni.user.models":{Alliance:[15,2,1,""],Coalition:[15,2,1,""],Corporation:[15,2,1,""],Group:[15,2,1,""],User:[15,2,1,""]},"sni.user.models.Alliance":{SCHEMA_VERSION:[15,3,1,""],_version:[15,3,1,""],alliance_id:[15,3,1,""],alliance_name:[15,3,1,""],authorized_to_login:[15,3,1,""],ceo:[15,4,1,""],coalitions:[15,4,1,""],executor:[15,4,1,""],executor_corporation_id:[15,3,1,""],mandatory_esi_scopes:[15,3,1,""],ticker:[15,3,1,""],updated_on:[15,3,1,""],user_iterator:[15,4,1,""],users:[15,4,1,""]},"sni.user.models.Coalition":{SCHEMA_VERSION:[15,3,1,""],_version:[15,3,1,""],authorized_to_login:[15,3,1,""],coalition_name:[15,3,1,""],created_on:[15,3,1,""],mandatory_esi_scopes:[15,3,1,""],members:[15,3,1,""],ticker:[15,3,1,""],updated_on:[15,3,1,""],user_iterator:[15,4,1,""],users:[15,4,1,""]},"sni.user.models.Corporation":{SCHEMA_VERSION:[15,3,1,""],_version:[15,3,1,""],alliance:[15,3,1,""],authorized_to_login:[15,3,1,""],ceo:[15,4,1,""],ceo_character_id:[15,3,1,""],corporation_id:[15,3,1,""],corporation_name:[15,3,1,""],mandatory_esi_scopes:[15,3,1,""],ticker:[15,3,1,""],updated_on:[15,3,1,""],user_iterator:[15,4,1,""],users:[15,4,1,""]},"sni.user.models.Group":{SCHEMA_VERSION:[15,3,1,""],_version:[15,3,1,""],authorized_to_login:[15,3,1,""],created_on:[15,3,1,""],description:[15,3,1,""],discord_role_id:[15,3,1,""],group_name:[15,3,1,""],is_autogroup:[15,3,1,""],map_to_discord:[15,3,1,""],map_to_teamspeak:[15,3,1,""],members:[15,3,1,""],owner:[15,3,1,""],teamspeak_sgid:[15,3,1,""],updated_on:[15,3,1,""]},"sni.user.models.User":{SCHEMA_VERSION:[15,3,1,""],_version:[15,3,1,""],alliance:[15,4,1,""],authorized_to_login:[15,3,1,""],character_id:[15,3,1,""],character_name:[15,3,1,""],clearance_level:[15,3,1,""],coalitions:[15,4,1,""],corporation:[15,3,1,""],created_on:[15,3,1,""],cumulated_mandatory_esi_scopes:[15,4,1,""],discord_user_id:[15,3,1,""],is_ceo_of_alliance:[15,4,1,""],is_ceo_of_corporation:[15,4,1,""],teamspeak_cldbid:[15,3,1,""],tickered_name:[15,4,1,""],updated_on:[15,3,1,""]},"sni.user.signals":{on_coalition_post_save:[15,1,1,""],on_user_post_save:[15,1,1,""]},"sni.user.user":{ensure_alliance:[15,1,1,""],ensure_autogroup:[15,1,1,""],ensure_corporation:[15,1,1,""],ensure_user:[15,1,1,""]},"sni.utils":{callable_from_name:[11,1,1,""],catch_all:[11,1,1,""],catch_all_async:[11,1,1,""],catches_all:[11,1,1,""],from_timestamp:[11,1,1,""],now:[11,1,1,""],now_plus:[11,1,1,""],random_code:[11,1,1,""]},sni:{__main__:[11,0,0,"-"],conf:[11,0,0,"-"],scheduler:[11,0,0,"-"],utils:[11,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","function","Python function"],"2":["py","class","Python class"],"3":["py","attribute","Python attribute"],"4":["py","method","Python method"],"5":["py","data","Python data"],"6":["py","exception","Python exception"]},objtypes:{"0":"py:module","1":"py:function","2":"py:class","3":"py:attribute","4":"py:method","5":"py:data","6":"py:exception"},terms:{"24h":1,"2c48822e0a1b":6,"43c5":6,"478b":1,"48h":1,"4df0":1,"8pmzcetkb4vfudrhlc":6,"998e12c7":6,"abstract":14,"byte":14,"case":3,"catch":11,"class":[0,5,6,8,10,12,14,15],"default":[3,5,6,11],"enum":[6,14],"export":7,"function":[0,5,7,11],"import":[10,11],"int":[0,4,5,6,10,11,12,14,15],"new":[0,4,5,6,12,14],"null":[3,5],"public":[6,14],"return":[0,4,5,6,10,11,12,14,15],"short":[0,5,7],"static":[0,6,7],"true":[3,6,14],"try":5,"while":14,EVE:[0,3,7,8,14,15],For:[4,7,14],IDs:6,Its:7,NOT:[6,15],Not:3,That:0,The:[0,1,3,5,6,7,10,11,12,13,14],Then:7,There:1,These:5,Use:[5,13,14],__main__:11,_cl:5,_id:[13,14],_sender:[4,11,15],_test_tick:11,_test_tock:11,_version:[0,4,6,8,10,15],a8b9:1,aaaaaaaa:3,about:[0,14],absolut:14,absolutescop:14,abstractscop:14,access:[5,6,7],access_token:6,accord:[6,8,15],account:5,act:4,action:14,actual:14,add_job:11,add_memb:0,added:[3,5],addit:14,admin:3,administr:[0,14],aezxdswm:6,affili:7,after:1,against:[5,7,14],aka:15,akin:12,algorithm:3,all:[0,1,4,5,6,7,8,11,12,14,15],all_pag:0,allianc:[6,7,13,14,15],alliance_id:[0,6,15],alliance_nam:15,allow:[14,15],along:[6,8],alreadi:[4,5],also:[0,1,5,11,12,15],altari:7,altern:[5,7],although:15,alwai:[6,14],ani:[0,4,6,11,12,14,15],annot:6,anoth:14,anyhttpurl:0,anyth:[4,5],api:[1,3,5,6,7,13],app:[0,1,3,7,14],app_token:14,appli:14,applic:[0,1,3,5,6,7,8,10,14,15],appropri:0,apschedul:[0,11],are_in_same_alli:14,are_in_same_coalit:14,are_in_same_corpor:14,arg:[0,5,6,8,10,11,12,14,15],argpars:11,argument:[6,7,11,14],arrai:14,ask:[5,12],assert:14,assert_has_clear:14,assert_is_set:11,asset:6,assign:12,associ:[5,15],assum:15,asteroid_belt:6,asteroid_belt_id:6,async:[0,5,11],asyncio:5,asyncron:11,attach:6,attack:0,auth:[0,3,5],auth_channel_id:3,auth_group_nam:3,auth_role_nam:3,authent:[0,3,5,7,12,14],authentication_sourc:3,author:[0,1,5,6,14],authorizationcoderespons:6,authorized_to_login:[0,14,15],autogroup:15,automat:[3,5,12,15],available_esi_scop:[0,6],azp:6,backend:7,baee74e2d517:1,balanc:8,base:[0,5,6,7,8,10,12,14,15],basemodel:[0,6,12],bash:7,basic:[11,14],bearer:[1,6,14],becaus:5,been:[5,11,14],befor:[5,10],being:0,belong:[3,14,15],bit:8,bloke:6,bodi:[0,8],bookmark:6,bool:[0,4,6,14,15],bot:[3,7,11],bot_id:5,bot_nam:3,both:14,bound:12,bsonobjectid:0,bz2:10,c_a:11,c_b_x:11,c_b_y:11,cach:12,cached_teamspeak_queri:12,calendar:6,call:[0,4,5,6,11,12,14],callabl:[11,12],callable_from_nam:11,callable_nam:0,callback:[7,14],can:[0,1,3,5,10,14,15],cannot:0,cascad:5,catch_al:11,catch_all_async:11,catches_al:11,ceo:[14,15],ceo_character_id:15,certain:6,challeng:[0,5,12],challenge_nicknam:[0,12],chang:[3,5,7,12,14],channel:[3,5],charact:[0,6,8,15],character_id:[0,1,6,8,10,15],character_nam:[0,11,15],characterstat:6,check:[5,7,10,11,12,14],checksum:10,cid:12,clean:[5,11],cleanup:5,clear:[5,11],clearanc:[0,7,15],clearance_level:[0,15],clearancemodificationscop:14,clid:12,client:[0,3,4,5,10,12],client_database_id:12,client_id:[3,5,6],client_list:12,client_nicknam:12,client_secret:[3,6],client_typ:12,clone:6,coalesc:0,coalit:[7,13,14,15],coalition_id:0,coalition_nam:[0,15],code:[0,5,6,7,13,14],collect:[0,4,6,8,10,15],collection_nam:4,com:[3,5,6,7],combin:8,command:[3,7,11],comment:[0,14],common:[0,14],commun:[6,7],complet:[0,5,12],complete_authentication_challeng:[5,12],compos:7,concurr:11,condit:14,conf:11,config:11,configur:[5,7],configure_log:11,conjunct:0,connect:[4,6,10,12],connect_database_sign:11,connect_via:11,connector:7,consid:[5,14],contain:[0,6,7,11,14],container_nam:7,contract:6,control:7,convert:[0,6],copror:15,core:7,corp:[0,6],corpor:[6,7,14,15],corporation_id:[0,6,15],corporation_nam:15,correct:11,correspond:[5,6,8,12,14,15],cought:0,crash:0,crashreport:0,crashreportrequest:0,crashreporttoken:0,creat:[0,3,4,5,6,7,11,12,14,15],create_dynamic_app_token:14,create_permanent_app_token:14,create_state_cod:14,create_user_token:14,created_on:[0,5,6,12,14,15],createus:7,creation:[5,6,12,14,15],credit:11,crope:6,cumulated_mandatory_esi_scop:[0,15],current:[0,4,8,11,12],custom:7,data:[0,6,7,14,15],databas:[3,7,11],date:15,datetim:[0,4,11],dcbd81af:1,debug:[3,11],declar:14,decod:6,decode_access_token:6,decodedaccesstoken:6,decompress:10,decor:11,decreas:0,dedic:5,def:11,delet:[0,5,6],delete_coalit:0,delete_group:0,delete_token:0,delete_us:0,demot:[5,14],deni:5,depend:[0,5,14],derefer:5,dereferenc:5,deriv:[1,6,14],descript:[0,15],detail:0,determin:14,develop:[3,5,7,10],dict:[0,6,11],dictfield:5,dictionnari:11,differ:[5,14],digit:11,direct:5,disconnect:5,discorb:3,discord:[3,7,11,15],discord_role_id:15,discord_us:5,discord_user_id:15,discordauthenticationchalleng:5,discort:5,distance_penalti:14,do_noth:5,doc:6,docker:7,docstr:13,document:[0,4,5,6,8,10,11,12,13,14,15],doe:[4,5,11,14,15],doesn:[5,12],doesnotexist:6,domain:7,don:[5,7],done:[0,1,12],download:10,download_latest_sd:10,dump:10,dump_path:10,dure:0,dyn:[0,14],dynam:[0,1,14],each:14,easiest:7,editor:9,element:0,els:[11,14],email:8,embeddeddocu:[0,5,8],enabl:3,end:14,ensur:[5,12,14,15],ensure_alli:15,ensure_alliance_memb:15,ensure_alliances_memb:15,ensure_autogroup:15,ensure_corpor:15,ensure_corporation_memb:15,ensure_corporations_memb:15,ensure_group:12,ensure_minimum_vers:4,ensure_role_for_group:5,ensure_root:15,ensure_root_dyn_token:14,ensure_root_per_token:14,ensure_superuser_group:15,ensure_us:15,entri:[7,13],enumer:14,environ:7,error:11,error_messag:11,esi:[1,3,7,10,11,13,14,15],esi_access_token:6,esi_annot:6,esi_delet:6,esi_delete_on_befalf_of:6,esi_get:6,esi_get_all_pag:6,esi_get_on_befalf_of:6,esi_object_nam:10,esi_path:0,esi_post:6,esi_post_on_befalf_of:6,esi_put:6,esi_put_on_befalf_of:6,esi_refresh_token:6,esi_request:6,esi_request_on_behalf_of:6,esi_respons:6,esi_scop:6,esiaccesstoken:6,esicharacterloc:8,esimail:8,esimailrecipi:8,esiobjectnam:10,esipath:6,esirefreshtoken:6,esirequestin:0,esirespons:6,esiscop:14,esiskillpoint:8,esitokenerror:6,esiwalletbal:8,especi:5,etc:[0,6,7],eve:15,even:7,event:[7,11],eveonlin:6,everyon:14,everytim:5,evetech:6,exampl:[6,7,11],except:[0,6,11],exception_handl:0,exec:7,execut:5,executor:[0,14,15],executor_corporation_id:15,exist:[4,5,12,14,15],exp:6,expir:[1,6,10],expiration_datetim:0,expires_in:6,expires_on:[0,6,10,14],explanatori:[14,15],exporti:10,express:6,extract:6,eyjhbgcioijiuzi1niisin:1,facil:11,fact:0,fals:[0,3,5,6,11,14],fastapi:14,fetch:[0,10,15],field:[0,4,5,6,8,10,13,14,15],field_id:10,field_nam:[4,10],file:[7,9,11],find_client:12,find_group:12,fit:6,flatten:11,flatten_dict:11,fleet:6,fly:8,follow:[2,5,7,11,12,14],forget:7,form:[1,6,7],formal:15,format:[3,8],format_mail_bodi:8,forward:0,found:[6,12],from:[0,1,3,5,6,10,11,14,15],from_authotization_head:[0,14],from_authotization_header_nondyn:[0,14],from_id:8,from_job:0,from_record:0,from_respons:6,from_timestamp:11,from_user_iter:0,frontend:[0,7],furthermor:14,gener:[3,7],get:[0,1,5,6,11,14],get_access_token:[6,13],get_access_token_from_callback_cod:[6,13],get_alliance_track:0,get_auth_url:6,get_basic_authorization_cod:6,get_callback_esi:0,get_coalit:0,get_coalition_nam:0,get_coalition_track:0,get_corporation_track:0,get_esi_latest:0,get_esi_path_scop:6,get_group:0,get_group_nam:0,get_guild:5,get_job:0,get_latest_sde_md5:10,get_memb:5,get_p:0,get_pymongo_collect:4,get_token:0,get_token_from_jwt:14,get_us:0,get_user_nam:0,getcoalitionout:0,getcoalitionshortout:0,getgroupout:0,getgroupshortout:0,getjobout:0,gettokenout:0,gettrackingout:0,getuserout:0,getusershortout:0,git:7,git_url:7,github:[7,13],given:[0,4,5,6,8,11,14,15],global:[11,14],goe:6,good:[0,6],grant:14,graphic:6,graphic_fil:6,graphic_id:6,group:[3,5,7,12,13,14,15],group_id:[0,12],group_list:12,group_nam:[0,15],grp:[0,5],guild:5,handl:[5,6],handler:[5,7,11],happen:5,has:[0,4,5,6,8,11,12,14],has_a_valid_refresh_token:6,has_clear:14,has_esi_scop:6,has_no_refresh_token:6,has_outdated_docu:4,hash:10,have:[0,4,5,6,9,10,11,14,15],header:[0,1,6,14],help:2,here:[3,8,9],hex:3,hierarch:14,his:14,host:3,how:14,hs256:3,html:[6,8],http:[0,3,5,6,7,14],http_method:6,iconid:12,id_annot:[0,6],idididididididididididididididid:3,imag:7,immedi:11,implement:5,import_sde_dump:10,import_sde_dump_inv_categori:10,import_sde_dump_inv_constel:10,import_sde_dump_inv_group:10,import_sde_dump_inv_solar_system:10,import_sde_dump_inv_typ:10,import_sde_dump_map_region:10,imran:11,inact:1,includ:[1,7],index:[0,7],index_user_loc:8,index_user_mail:8,index_user_skillpoint:8,index_user_wallet:8,index_users_loc:8,index_users_mail:8,index_users_skillpoint:8,index_users_wallet:8,indexact:8,indic:14,industri:6,info:3,inform:[0,14,15],inherit:1,init:11,init_mongodb:4,initi:[6,12],instanc:[0,4,14],instead:[13,14,15],integ:[5,8,14],interfac:[6,7],interv:11,invalid:[6,14],invalid_refresh_token:0,invalidate_token_on_error:6,invaliddocumenterror:5,invcategori:10,invgroup:10,invit:5,invtyp:10,is_authorized_to_login:[14,15],is_autogroup:[0,15],is_ceo_of_alli:[0,15],is_ceo_of_corpor:[0,15],iss:6,issu:[0,3,6,14],item:8,iter:[0,6,12,15],its:[0,4,5,6,11,12,14,15],jitter:11,job:[7,11],job_id:0,jobs_kei:[5,11],json:6,jti:6,just:7,jwt:[1,3,6,13,14],jzozkrta8b:6,kei:[5,6,11],kid:6,killmail:6,kind:1,known:5,kwarg:[0,4,6,8,11,12,15],last:[0,6,15],latest:[0,6,8,10,15],layer:[4,6],lazili:5,lazyreferencefield:5,lead:5,least:14,length:11,less:4,letter:11,level:[0,14,15],like:[1,5,6,11,14],line:[7,11,13],link:5,list:[0,5,6,7,8,11,12,15],listen:3,listfield:5,load:[6,11],load_configuration_fil:11,load_esi_openapi:6,locat:[3,6,8,13],log:[1,3,5,11,14],log_channel_id:[3,5],logging_level:3,login:[6,14,15],login_url:0,look:[1,5,6],lookuperror:12,lowercas:11,lqjg2:6,made:[0,11],magic:4,mai:15,mail:[6,8],mail_id:8,main:7,make:[0,5,6,7,11,15],manag:[0,5,7,11,12],manage_planet:6,mandatori:15,mandatory_esi_scop:[0,15],manual:[0,1,15],map:[5,6,10,15],map_teamspeak_group:12,map_to_discord:[5,15],map_to_teamspeak:15,mapconstel:10,mapfield:5,mapregion:10,mapsolarsystem:10,market:6,match:[7,12],matter:14,max_inst:0,md5:10,mean:[5,6],measur:8,member:[0,5,11,14,15],membership:12,messag:[3,5,11,12],message_registered_clients_with_wrong_nam:12,metadata:[6,14],method:[0,5,6,12,14,15],migrat:[7,11],migrate_alli:15,migrate_coalit:15,migrate_corpor:15,migrate_databas:11,migrate_esi_access_token:6,migrate_esi_refresh_token:6,migrate_group:15,migrate_us:15,minut:0,misfire_grace_tim:0,mode:3,model:[1,5,7,13],modif:0,modifi:5,mongo:7,mongo_cli:4,mongo_initdb_root_password:7,mongo_initdb_root_usernam:7,mongocli:4,mongodb:[3,7,11],mongoengin:[0,4,5,6,8,10,12,14,15],moon:6,moon_id:6,more:[0,6],most:[8,14],multipl:[6,12,13,15],must:[0,1,14],mutablemap:11,my3rdpartyclientid:6,name:[0,3,6,8,10,11,12,15],namespac:11,navi:3,necessari:[5,6],need:[6,10],nested_dict:11,net:6,new_authentication_challeng:[5,12],new_pymongo_cli:4,new_redis_connect:4,new_teamspeak_connect:12,next_run_tim:0,nice:7,nicknam:[0,5,12],no_refresh_token:0,non:0,none:[0,4,5,6,8,10,11,12,14,15],note:[1,5,7,14],notif:[0,1],notifi:[5,12,14],notimplementederror:14,now:11,now_plu:11,nullifi:5,oauth2:5,oauth:[0,6],object:[4,5,6,10,14,15],obtain:1,occur:0,odm:15,on_behalf_of:0,on_coalition_post_sav:15,on_disconnect:5,on_pre_sav:4,on_readi:5,on_user_post_sav:15,onc:[0,1],one:[5,14],onli:[4,5,14],onlin:[7,8],only_has_invalid_refresh_token:6,open_window:6,openapi:[0,6,7],openssl:3,oper:3,option:[0,4,5,6,10,12,14,15],order:[0,1],org:5,organize_mail:6,origin:[7,13],other:[7,14],otherwis:14,out:7,output:2,over:[0,15],own:[14,15],owner:[0,5,6,14,15],owner_character_id:0,owner_character_nam:0,page:[6,7],pagin:[13,15],param:0,paramet:[0,6],parent:[0,14],parent_kei:11,pars:[11,12],parse_command_line_argu:11,part:[14,15],pass:6,password:[3,7],path:[0,6,8,11],path_r:6,pdt:0,pend:5,per:[0,14],perform:[5,14],perman:[0,1,14],permiss:5,permissionerror:14,persist:8,planet:6,planet_id:6,player:15,plu:11,point:[7,8],pong:0,poor:5,popul:0,port:3,port_auth_start:0,portal:[3,5,7],post:[0,6],post_alli:0,post_auth_complet:0,post_coalit:0,post_corpor:0,post_group:0,post_job:0,post_sav:11,post_token_dyn:0,post_token_p:0,post_token_use_from_dyn:0,post_token_use_from_p:0,postauthstartout:0,postcallbackesiout:1,postcoalitionin:0,postgroupin:0,posttokendynin:0,posttokendynout:0,posttokenperin:0,posttokenperout:0,posttokenusefromdynin:0,posttokenusefromdynout:[0,1],postusefromperout:[0,1],precis:[5,6,14],predefin:0,prefix:15,present:5,preserv:14,pretermin:14,prevent:5,print:0,print_openapi_spec:0,priviledg:14,privileg:1,proce:[5,12],process:0,project:7,properti:[6,15],provid:14,publicdata:6,pull:[5,8],pumba:7,pure:14,put:[0,6],put_coalit:0,put_group:0,put_user_nam:0,putcoalitionin:0,putgroupin:0,putuserin:0,pwd:7,pydant:[0,6,12],pyjwt:3,pymongo:4,python3:2,python:0,python_main_modul:7,queri:[3,7,12,15],rais:[5,6,11,12,14],raise_for_statu:6,rand:3,random:[0,5,11],random_cod:11,rather:11,read:[6,14],read_agents_research:6,read_asset:6,read_blueprint:6,read_calendar_ev:6,read_character_bookmark:6,read_character_contract:6,read_character_job:6,read_character_min:6,read_character_ord:6,read_character_wallet:6,read_chat_channel:6,read_clon:6,read_contact:6,read_container_log:6,read_corporation_asset:6,read_corporation_bookmark:6,read_corporation_contract:6,read_corporation_job:6,read_corporation_killmail:6,read_corporation_membership:6,read_corporation_min:6,read_corporation_ord:6,read_corporation_rol:6,read_corporation_wallet:6,read_customs_offic:6,read_divis:6,read_facil:6,read_fatigu:6,read_fit:6,read_fleet:6,read_fw_stat:6,read_impl:6,read_killmail:6,read_loc:6,read_loyalti:6,read_mail:6,read_med:6,read_notif:6,read_onlin:6,read_opportun:6,read_ship_typ:6,read_skil:6,read_skillqueu:6,read_stand:6,read_starbas:6,read_structur:6,read_titl:6,readi:5,readwrit:7,real:0,realli:[11,15],receiv:0,recipi:8,recipient_id:8,recipient_typ:8,record:[0,15],recurr:[10,12],recurs:6,redi:[3,5,7,11],redirect:0,refer:[0,4,5,6,7,8,14,15],referenc:5,referencefield:5,refresh:[0,6,7],refresh_access_token:6,refresh_token:[6,11],regard:[0,6],regardless:14,regis:14,regist:[5,7,12],register_delete_rul:5,regular:6,relat:[0,4,5,6,10,14,15],relev:[6,10,15],remeb:14,remov:8,remove_memb:0,repackag:8,repli:0,repons:[0,6],report:[0,6,12],repres:[0,5,6,8,10,12,14,15],represent:[0,11,12],request:[0,1,6],requir:[0,1,5,6,7,14,15],reset:[14,15],reset_clear:14,resort:0,respond_calendar_ev:6,respons:[0,1,6],ressourc:10,rest:7,result:[6,12,13,14,15],retriev:[5,14],reverse_delete_rul:5,revok:1,rguc:6,role:[5,7,15],root:[1,3,7,14,15],root_url:3,rootpassword:7,router:[1,7,13],rule:5,run:[0,2,5,6,8,10,11,12],run_schedul:11,run_tim:[5,11],run_times_kei:[5,11],same:[6,12,14],satisfi:14,save:[0,6,14,15],save_esi_token:6,savedb:12,schedul:[0,5,6,7,8],schedule_job:11,scheduler_thread_count:3,schema:[0,4,6,8,10,14,15],schema_vers:[0,4,6,8,10,15],scope:[0,5,7,13,14,15],scope_level:14,scope_nam:14,scp:6,sde:[6,10],sde_get_nam:[6,10],search:[6,7,8],search_structur:6,seat:3,second:[5,11,12],secret:3,secretsecretsecretsecretsecretsecret0000:3,secretsecretsecretsecretsecretsecretsecretsecretsecretsecret0000:3,see:[0,1,3,4,5,6,7,8,10,12,14,15],self:[14,15],send:[3,5,12],send_mail:6,sender:8,sent:1,separ:11,server:[3,7,12],server_id:[3,5],servic:7,set:[3,4,5,6,11,14,15],set_if_not_exist:4,sgid:12,shell:7,ship:8,ship_item_id:8,ship_nam:8,ship_type_id:8,should:[0,1,3,5,6,14,15],signal:[7,11],signatur:6,similar:[0,13],simpler:7,simpli:[11,15],simplist:7,singl:15,skill:[6,8],skillpoint:8,sni:[1,2,3,4,5,6,8,10,12,13,15],snipassword:[3,7],solar:8,solar_system_id:[6,8,10],solv:5,some:[0,6,14],someth:6,sourc:[0,4,5,6,8,10,11,12,14,15],specif:[0,3,6,7,14],specifi:[0,4,11],sqlite3:10,sqlite:10,src:7,sso:[0,1,7,13,14],stage:6,star:6,star_id:6,stargat:6,stargate_id:6,start:[0,5,11,12],start_api_serv:0,start_bot:5,start_discord_bot:11,start_schedul:[5,11],state:[0,6,14],state_cod:[0,1],statecod:[12,13,14],station:[6,8],station_id:[6,8],statu:[6,8,11,14],status_cod:6,still:0,stop:[5,11],stop_schedul:[5,11],store:[5,7,11],str:[0,4,5,6,8,10,11,12,14,15],string:[5,6,8,11,14],structir:8,structur:15,structure_id:8,structure_market:6,sub:6,subject:8,submit:0,submodul:11,subpackag:11,subsequ:1,sucess:12,suffici:14,suitabl:6,superior:14,superus:[14,15],support:[3,5,6,13],sure:[0,5,6,15],swagger:[6,9],syntax:5,system:[7,8],tabl:10,tag:8,take:1,target:14,task:[0,5,6,8,10,12,14],teamspeak:[3,7,10,15],teamspeak_cldbid:15,teamspeak_sgid:15,teamspeakauthenticationchalleng:12,teamspeakcli:12,teamspeakgroup:12,tell:[4,6,14,15],test:11,text:8,than:[4,14],thei:[14,15],them:0,themselv:1,therefor:5,thi:[0,1,3,5,6,7,8,10,11,12,14,15],thing:[5,11],thread:5,through:[3,6,12,15],thu:8,ticker:[0,15],tickered_nam:[0,15],tied:[0,1],time:[5,8,11],timedelta:11,timestamp:[0,5,6,8,11,12,14,15],tkn:[0,14],to_dict:0,to_jwt:14,todo:7,togeth:0,token:[1,3,7,12,13],token_has_enough_scop:6,token_str:14,token_typ:[0,6,14],tokentokentokentokentokentokentokentokentokentokentoken0000:3,tokentyp:[0,14],too:[0,13],total:8,total_sp:8,toward:6,trace:0,track:[0,6],track_memb:6,tracking_statu:[0,6],trackingstatu:6,trigger:0,ts3:12,ts3connect:12,ttl:12,tupl:[6,11],two:[1,14],type:[0,5,8,10,12,14],uac:[0,7,12,13,15],unalloc:8,unallocated_sp:8,uncaught:0,under:1,unicod:[5,8],univers:6,unix:11,unless:5,until:8,updat:[0,4,5,6,11,12,15],update_alliance_autogroup:15,update_alliance_from_esi:15,update_alliances_from_esi:15,update_coalition_autogroup:15,update_corpor:15,update_corporation_autogroup:15,update_discord_rol:5,update_discord_us:5,update_sd:10,update_teamspeak_group:12,update_user_autogroup:15,update_user_from_esi:15,update_users_from_esi:15,updated_on:[0,4,6,15],upon:0,uppercas:11,url:[0,3,6,14],urlsafe_b64encod:6,use:[0,1,7,11,14],used:[0,3,6,14,15],useful:5,user1:14,user2:14,user:[1,3,4,5,6,7,8,11,12,13],user_id:5,user_iter:15,user_token:[0,1],usernam:[3,7],using:[4,5],usr:[0,5,6,7,8,11,12,14,15],utc:11,util:7,uuid4:0,uuid:[0,12,13,14],valid:[0,1,6,13,14,15],valid_refresh_token:0,valu:[0,4,5,6,8,10,11,12,14,15],variou:[11,14],verif:14,version:[0,4,5,6,7,8,10,11,15],via:1,virtual:14,volum:7,wai:[7,14],wallet:[6,8],warn:14,web:[0,6,7],web_based_sso_flow:6,were:11,wether:[4,6,8,14,15],what:[5,14],when:[0,5,6,10,11,14],whenev:15,where:[0,3,8],which:[0,1,3,5,6,14],whichev:14,whose:[4,14],wish:1,workspac:13,wrapper:6,write:14,write_contact:6,write_fit:6,write_fleet:6,write_waypoint:6,wrong:6,yaml:[0,3,9,11],yes:15,yml:[3,7],you:[0,3,5],your:7},titles:["API Server","Authentication","Command line arguments","Configuration file reference","Database modules","Discord","ESI management","SeAT Navy Issue","ESI data indexation","OpenAPI specification","EVE Static Data Export management","Main SNI modules","Teamspeak","Todo list","User Access Control","User management"],titleterms:{"export":10,"static":10,EVE:[6,10],access:14,allianc:0,api:0,argument:2,authent:1,bot:5,callback:0,clearanc:14,coalit:0,command:[2,5],configur:[3,11],control:14,corpor:0,data:[8,10],databas:[0,4,5,6,8,10,12,14,15],discord:5,document:7,entri:11,esi:[0,6,8],event:5,exampl:3,file:3,gener:14,group:0,handler:[4,15],high:7,index:8,indic:7,issu:7,job:[0,5,6,8,10,12,15],level:7,line:2,list:13,main:[0,5,6,10,11,12,15],manag:[6,10,14,15],migrat:[0,4,5,6,8,10,12,14,15],model:[0,6,8,10,12,14,15],modul:[0,4,5,6,7,10,11,12,15],mongodb:4,navi:7,openapi:9,other:11,point:11,redi:4,refer:3,router:0,run:7,schedul:11,scope:6,seat:7,server:0,signal:[0,4,5,6,8,10,12,14,15],sni:[0,7,11,14],specif:9,sso:6,system:0,tabl:7,teamspeak:[0,12],todo:[0,6,13,14,15],token:[0,6,14],uac:14,user:[0,14,15],util:[4,11,14]}})