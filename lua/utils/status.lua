#!/usr/bin/env luajit

local curl = require"cURL"
local json = require"cjson"
local i = require"inspect" -- luacheck: no unused

local root = arg[1] or "."
-- ^ I'd used autodetection based on arg[0] (path to script), but io.open doesn't support "/../"'s on path'
local api  = root.."/public/api"


local cfg_f = root.."/config.json"
local cfg_fd, _ = io.open(cfg_f,"r")
if not(cfg_fd) then print("Failed to load config"); os.exit(1) end
local cfg_s=cfg_fd:read"*a"
if #cfg_s<3 then print("empty config"); os.exit(2) end
local cfg = json.decode(cfg_s)
if not(cfg) or not(cfg.castNicks) then print("broken config"); os.exit(3) end
cfg_fd:close()


-- Functions {{{

local function notify(msg,important) -- {{{
	local cast
	if important then
		local cast_nicks = table.concat(cfg.castNicks, ", ")
		cast = ("\n\nCast %s"):format(cast_nicks)
	else
		cast = ""
	end
	local c = curl.easy{
		url        = cfg.slackHookURL,
		post       = true,
		followlocation = true,
		httpheader = {
			"Content-Type: application/json",
		},
		postfields = json.encode{
			username   = "Проверка состояния прокси",
			channel    = cfg.slackChanName,
			icon_emoji = ":warning:",
			text       = tostring(msg)..cast,
		},
		writefunction = function() end,
	}
	-- print(i(msg))
	c:perform()
end -- }}}

local function getList() -- {{{
	local fd, err = io.open(("%s/proxy/list/index.json"):format(api),"r")
	if not(fd) then
		print("Error:",err)
		notify(("Возникла ошибка при чтении списка проксей: ```%s```"):format(err), true)
		os.exit(1)
	end
	local ret = fd:read"a*"
	fd:close()
	return ret
end -- }}}

local function setActivity(name, status) -- {{{
	local buf=""
	local c = curl.easy{
		url             = ("https://app.censortracker.org/api/proxy/update/%s/"):format(name),
		post            = true,
		customrequest   = "PATCH",
		followlocation  = true,
		httpheader      = {
			("Authorization: %s"):format(cfg.apiAuth),
			"Content-Type: application/json",
		},
		postfields      = json.encode{
			active = status
		},
		writefunction   = function(r) buf=buf..r end,
		-- verbose = true,
	}
	local ok, err = pcall(c.perform,c)
	if not(ok) then
		notify(("Не получилось выставить активность для прокси `%s`.\n\nОшибка: ```%s```"):format(name, err), true)
	elseif c:getinfo(curl.INFO_RESPONSE_CODE) ~= 200 then
		notify(("Не получилось выставить активность для прокси `%s`.\n\nОтвет сервера: ```%s```"):format(name, buf), true)
	end
end -- }}}

local function setStatus(pt, status) -- {{{
	local proxyName = pt.name

	local fd, err = io.open(("%s/proxy/status/%s/index.json"):format(api, proxyName),"w+")
	if not(fd) then
		print("Error:", err)
		notify(("Возникла ошибка при записи статуса прокси в файл %q. Текст ошибки: ```%s```"):format(proxyName, err), true)
		os.exit(1)
	end
	fd:write(json.encode(status))
	fd:close()
	if pt.active ~= status.alive then
		setActivity(proxyName, status.alive)
	end
end -- }}}

local function checkProxy(pt) -- {{{
	local ret = { -- luacheck: no unused
		alive = false,
		code = 999,
		color = "gray"
	}
	local c = curl.easy{
		url             = "https://censortracker.org",
		proxy           = ("https://%s:%d"):format(pt.server, pt.port),
		timeout = 10,
		connecttimeout = 10,
		writefunction  = function() end
	}
	local ok, err = pcall(c.perform, c)
	local retcode = c:getinfo(curl.INFO_RESPONSE_CODE)
	if not(ok) then
		local e = err:gsub("^%[CURL[^%]]+%]","")
		ret = {
			alive = false,
			error_text = e,
			code = 1,
			color = "red",
		}
		notify(
			("При проверке прокси `%s` обнаружена проблема. От cURL была получена ошибка: ```%s```"):format(pt.name, e),
			true
		)
	elseif retcode ~= 200 then
		ret = {
			alive = true,
			color = "yellow",
			code = 2,
		}
		notify(
			("Сайт censortracker.org при проверке через прокси `%s` почему-то вернул HTTP-код %d (вместо 200)")
				:format(pt.name, retcode),
			true
		)
	else
		ret = {
			alive = true,
			color = "green",
			code = 0,
		}
	end
	return ret
end -- }}}

-- }}}

local list    = getList()
local proxies = json.decode(list)

for _,v in ipairs(proxies) do
	if v.weight > 0 then
		local status = checkProxy(v)
		setStatus(v,status)
	end
end
