#pragma once
#include <optional>
#include <string>
#include <json/json.h>

struct UpdateUserRequestDto {
	std::optional<std::string> email;
	std::optional<std::string> login;
	std::optional<int> role;

	static std::optional<UpdateUserRequestDto> fromJson(const Json::Value & json)
	{
		if (!json.isObject())
			return std::nullopt;

		if (!json.isMember("email") || !json["email"].isString())
			return std::nullopt;

		if (!json.isMember("login") || !json["login"].isString())
			return std::nullopt;

		UpdateUserRequestDto dto;
		dto.email = json["email"].asString();
		dto.login = json["login"].asString();
		dto.role = json["role"].asString();

		return dto;
	}
};