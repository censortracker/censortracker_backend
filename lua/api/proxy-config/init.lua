-- luacheck: globals ngx
local root = ngx.var.document_root;
local dict_name = ngx.var.ct_srv_dict;
local servers = ngx.shared[dict_name];
local list, upts;

local cjson = cjson or require"cjson" -- luacheck: globals cjson

local ts = ngx.time()
list = servers:get"list"
upts = servers:get"upts"

math.randomseed(ts)

-- TODO: причесать это всё и разложить по субдиректориям, чтобы была более модульная инфраструктура и более читаемый код

local function fallback(reason)
	-- TODO: отправить в телегу и слак
	local _ = reason -- TODO: причина фейла (для выбора разных сообщений в телегу и слак)
	ngx.status=500
	ngx.header.Content_Type = "application/json";

	ngx.print(("%s"):format(
		cjson.encode(
			{ -- фоллбек
				server="proxy-fallback.censortracker.org",
				port="33333",
				pingHost="proxy-fallback.censortracker.org",
				pingPort="39263",
				fallbackReason=reason,
			}
		)
	))

	ngx.exit(500)
end


if -- если
	not(list) or -- нет кеша списка серверов или
	not(upts) or -- нет таймштампа последнего обновления списка или
	( ( tonumber(upts) + 20 ) < ts ) -- список обновлён больше 20 секунд назад
then
	local fd, _ =io.open(root.."/public/api/proxy/list/index.json","r")
	if not(fd) then -- если всё сломалось (файл не смог открыться).
		-- Вообще, такого, по идее, происходить не должно, файл-то статичный.
		-- Разве что если повредится при переполнении диска 🤷
		fallback("noList")
	end

	list = fd:read"a*"
	fd:close()

	if #list<10 then fallback("brokenList") end

	servers:set("list",list)
	servers:set("upts",ts)
end

local excluded = {}
local query = ngx.req.get_uri_args();
local exc = query.exclude
if exc then
	if type(exc) == "string" then
		excluded[exc] = true
	elseif type(exc) == "table" then
		for _,v in ipairs(exc) do
			excluded[v] = true
		end
	end
end

--[[
local function contains(t,w)
	for _,v in ipairs(t) do
		if v == w then return true end
	end
	return false
end
 ]]

-- Наполнение списка
local proxies = cjson.decode(list)
local randlist = {}
for _,v in ipairs(proxies) do
	if v.active and not(excluded[v.server]) then
		local w = v.weight;
		for _=1,w do
			v.weight = nil
			v.active = nil
			table.insert(randlist, v)
		end
	end
end

if #randlist == 0 then fallback("noMore") end

-- Ответ
ngx.status = 200
ngx.header.Content_Type = "application/json";

local ret = randlist[math.random(#randlist)]
ret.excludedServers = #excluded>0 and excluded

ngx.print(("%s"):format(cjson.encode(ret)))
ngx.exit(ngx.status)
