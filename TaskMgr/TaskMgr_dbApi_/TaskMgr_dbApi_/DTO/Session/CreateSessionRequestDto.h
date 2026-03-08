#pragma once
#include <string>
#include <json/json.h>

struct CreateSessionRequestDto
{
    std::string loginOrEmail;
    std::string password;

    static CreateSessionRequestDto fromJson(const Json::Value& json)
    {
        CreateSessionRequestDto dto;

        dto.loginOrEmail = json.get("loginOrEmail", "").asString();
        dto.password = json.get("password", "").asString();

        return dto;
    }
};