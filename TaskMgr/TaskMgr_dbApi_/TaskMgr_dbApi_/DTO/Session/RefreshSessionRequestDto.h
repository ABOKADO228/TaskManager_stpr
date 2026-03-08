#pragma once
#include <string>
#include <json/json.h>

struct RefreshSessionRequestDto
{
    std::string refreshToken;

    static RefreshSessionRequestDto fromJson(const Json::Value& json)
    {
        RefreshSessionRequestDto dto;
        dto.refreshToken = json.get("refreshToken", "").asString();
        return dto;
    }
};