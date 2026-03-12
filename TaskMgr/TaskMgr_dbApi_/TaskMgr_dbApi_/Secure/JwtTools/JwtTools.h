#pragma once

#include <optional>
#include <string>
#include <memory>
#include <chrono>
#include <iomanip>
#include <sstream>
#include <cstdint>

#include <openssl/evp.h>
#include <openssl/hmac.h>
#include <json/json.h>

#include "../Models/User.h"
#include "../JwtTools/JwtConfig.h"

class JwtTools
{
public:
    JwtTools() = default;
    ~JwtTools() = default;

    static std::string hashPassword(const std::string& password) {
        return sha256Hex(password + "::salt");
    }

    static std::string createJwt(const User& user) {
        Json::Value header;
        header["alg"] = "HS256";
        header["typ"] = "JWT";

        Json::Value payload;
        payload["sub"] = user.id;
        payload["email"] = user.email;
        payload["role"] = user.role;
        payload["iss"] = jwtConf::kJwtIssuer;
        payload["exp"] = static_cast<Json::Int64>(nowEpoch() + jwtConf::kAccessTtlSec);

        Json::StreamWriterBuilder writerBuilder;
        writerBuilder["indentation"] = "";

        std::string h = base64UrlEncode(Json::writeString(writerBuilder, header));
        std::string p = base64UrlEncode(Json::writeString(writerBuilder, payload));
        std::string data = h + "." + p;
        std::string sig = base64UrlEncode(hmacSha256(jwtConf::kJwtSecret, data));

        return data + "." + sig;
    }

    static std::optional<Json::Value> verifyJwt(const std::string& token) {
        auto p1 = token.find('.');
        if (p1 == std::string::npos) {
            return std::nullopt;
        }

        auto p2 = token.find('.', p1 + 1);
        if (p2 == std::string::npos) {
            return std::nullopt;
        }

        std::string h = token.substr(0, p1);
        std::string p = token.substr(p1 + 1, p2 - p1 - 1);
        std::string s = token.substr(p2 + 1);

        std::string expected = base64UrlEncode(
            hmacSha256(jwtConf::kJwtSecret, h + "." + p)
        );

        if (expected != s) {
            return std::nullopt;
        }

        std::string payloadRaw = base64UrlDecode(p);
        if (payloadRaw.empty()) {
            return std::nullopt;
        }

        Json::Value payload;
        Json::CharReaderBuilder readerBuilder;
        std::string errs;
        std::unique_ptr<Json::CharReader> reader(readerBuilder.newCharReader());

        bool ok = reader->parse(
            payloadRaw.data(),
            payloadRaw.data() + payloadRaw.size(),
            &payload,
            &errs
        );

        if (!ok) {
            return std::nullopt;
        }

        if (!payload.isMember("exp") || !payload.isMember("sub") || !payload.isMember("iss")) {
            return std::nullopt;
        }

        if (payload["iss"].asString() != jwtConf::kJwtIssuer) {
            return std::nullopt;
        }

        if (payload["exp"].asInt64() < nowEpoch()) {
            return std::nullopt;
        }

        return payload;
    }

private:
    static std::int64_t nowEpoch() {
        return std::chrono::duration_cast<std::chrono::seconds>(
            std::chrono::system_clock::now().time_since_epoch()
        ).count();
    }

    static std::string base64UrlEncode(const std::string& input) {
        std::string out;
        out.resize(4 * ((input.size() + 2) / 3));

        int len = EVP_EncodeBlock(
            reinterpret_cast<unsigned char*>(out.data()),
            reinterpret_cast<const unsigned char*>(input.data()),
            static_cast<int>(input.size())
        );

        out.resize(len);

        for (char& c : out) {
            if (c == '+') {
                c = '-';
            }
            else if (c == '/') {
                c = '_';
            }
        }

        while (!out.empty() && out.back() == '=') {
            out.pop_back();
        }

        return out;
    }

    static std::string base64UrlDecode(std::string input) {
        for (char& c : input) {
            if (c == '-') {
                c = '+';
            }
            else if (c == '_') {
                c = '/';
            }
        }

        while (input.size() % 4 != 0) {
            input.push_back('=');
        }

        std::string out;
        out.resize((input.size() * 3) / 4);

        int len = EVP_DecodeBlock(
            reinterpret_cast<unsigned char*>(out.data()),
            reinterpret_cast<const unsigned char*>(input.data()),
            static_cast<int>(input.size())
        );

        if (len < 0) {
            return "";
        }

        out.resize(static_cast<std::size_t>(len));
        return out;
    }

    static std::string hmacSha256(const std::string& key, const std::string& data) {
        unsigned char hash[EVP_MAX_MD_SIZE];
        unsigned int len = 0;

        HMAC(
            EVP_sha256(),
            key.data(),
            static_cast<int>(key.size()),
            reinterpret_cast<const unsigned char*>(data.data()),
            static_cast<int>(data.size()),
            hash,
            &len
        );

        return std::string(reinterpret_cast<char*>(hash), len);
    }

    static std::string sha256Hex(const std::string& input) {
        unsigned char hash[EVP_MAX_MD_SIZE];
        unsigned int len = 0;

        EVP_MD_CTX* ctx = EVP_MD_CTX_new();
        if (!ctx) {
            return "";
        }

        if (EVP_DigestInit_ex(ctx, EVP_sha256(), nullptr) != 1) {
            EVP_MD_CTX_free(ctx);
            return "";
        }

        if (EVP_DigestUpdate(ctx, input.data(), input.size()) != 1) {
            EVP_MD_CTX_free(ctx);
            return "";
        }

        if (EVP_DigestFinal_ex(ctx, hash, &len) != 1) {
            EVP_MD_CTX_free(ctx);
            return "";
        }

        EVP_MD_CTX_free(ctx);

        std::ostringstream oss;
        for (unsigned int i = 0; i < len; ++i) {
            oss << std::hex
                << std::setw(2)
                << std::setfill('0')
                << static_cast<int>(hash[i]);
        }

        return oss.str();
    }
}; #pragma once

#include <optional>
#include <string>
#include <memory>
#include <chrono>
#include <iomanip>
#include <sstream>
#include <cstdint>

#include <openssl/evp.h>
#include <openssl/hmac.h>
#include <json/json.h>

#include "../Models/User.h"
#include "../JwtTools/JwtConfig.h"

class JwtTools
{
public:
    JwtTools() = default;
    ~JwtTools() = default;

    static std::string hashPassword(const std::string& password) {
        return sha256Hex(password + "::salt");
    }

    static std::string createJwt(const User& user) {
        Json::Value header;
        header["alg"] = "HS256";
        header["typ"] = "JWT";

        Json::Value payload;
        payload["sub"] = user.id;
        payload["email"] = user.email;
        payload["role"] = user.role;
        payload["iss"] = jwtConf::kJwtIssuer;
        payload["exp"] = static_cast<Json::Int64>(nowEpoch() + jwtConf::kAccessTtlSec);

        Json::StreamWriterBuilder writerBuilder;
        writerBuilder["indentation"] = "";

        std::string h = base64UrlEncode(Json::writeString(writerBuilder, header));
        std::string p = base64UrlEncode(Json::writeString(writerBuilder, payload));
        std::string data = h + "." + p;
        std::string sig = base64UrlEncode(hmacSha256(jwtConf::kJwtSecret, data));

        return data + "." + sig;
    }

    static std::optional<Json::Value> verifyJwt(const std::string& token) {
        auto p1 = token.find('.');
        if (p1 == std::string::npos) {
            return std::nullopt;
        }

        auto p2 = token.find('.', p1 + 1);
        if (p2 == std::string::npos) {
            return std::nullopt;
        }

        std::string h = token.substr(0, p1);
        std::string p = token.substr(p1 + 1, p2 - p1 - 1);
        std::string s = token.substr(p2 + 1);

        std::string expected = base64UrlEncode(
            hmacSha256(jwtConf::kJwtSecret, h + "." + p)
        );

        if (expected != s) {
            return std::nullopt;
        }

        std::string payloadRaw = base64UrlDecode(p);
        if (payloadRaw.empty()) {
            return std::nullopt;
        }

        Json::Value payload;
        Json::CharReaderBuilder readerBuilder;
        std::string errs;
        std::unique_ptr<Json::CharReader> reader(readerBuilder.newCharReader());

        bool ok = reader->parse(
            payloadRaw.data(),
            payloadRaw.data() + payloadRaw.size(),
            &payload,
            &errs
        );

        if (!ok) {
            return std::nullopt;
        }

        if (!payload.isMember("exp") || !payload.isMember("sub") || !payload.isMember("iss")) {
            return std::nullopt;
        }

        if (payload["iss"].asString() != jwtConf::kJwtIssuer) {
            return std::nullopt;
        }

        if (payload["exp"].asInt64() < nowEpoch()) {
            return std::nullopt;
        }

        return payload;
    }

private:
    static std::int64_t nowEpoch() {
        return std::chrono::duration_cast<std::chrono::seconds>(
            std::chrono::system_clock::now().time_since_epoch()
        ).count();
    }

    static std::string base64UrlEncode(const std::string& input) {
        std::string out;
        out.resize(4 * ((input.size() + 2) / 3));

        int len = EVP_EncodeBlock(
            reinterpret_cast<unsigned char*>(out.data()),
            reinterpret_cast<const unsigned char*>(input.data()),
            static_cast<int>(input.size())
        );

        out.resize(len);

        for (char& c : out) {
            if (c == '+') {
                c = '-';
            }
            else if (c == '/') {
                c = '_';
            }
        }

        while (!out.empty() && out.back() == '=') {
            out.pop_back();
        }

        return out;
    }

    static std::string base64UrlDecode(std::string input) {
        for (char& c : input) {
            if (c == '-') {
                c = '+';
            }
            else if (c == '_') {
                c = '/';
            }
        }

        while (input.size() % 4 != 0) {
            input.push_back('=');
        }

        std::string out;
        out.resize((input.size() * 3) / 4);

        int len = EVP_DecodeBlock(
            reinterpret_cast<unsigned char*>(out.data()),
            reinterpret_cast<const unsigned char*>(input.data()),
            static_cast<int>(input.size())
        );

        if (len < 0) {
            return "";
        }

        out.resize(static_cast<std::size_t>(len));
        return out;
    }

    static std::string hmacSha256(const std::string& key, const std::string& data) {
        unsigned char hash[EVP_MAX_MD_SIZE];
        unsigned int len = 0;

        HMAC(
            EVP_sha256(),
            key.data(),
            static_cast<int>(key.size()),
            reinterpret_cast<const unsigned char*>(data.data()),
            static_cast<int>(data.size()),
            hash,
            &len
        );

        return std::string(reinterpret_cast<char*>(hash), len);
    }

    static std::string sha256Hex(const std::string& input) {
        unsigned char hash[EVP_MAX_MD_SIZE];
        unsigned int len = 0;

        EVP_MD_CTX* ctx = EVP_MD_CTX_new();
        if (!ctx) {
            return "";
        }

        if (EVP_DigestInit_ex(ctx, EVP_sha256(), nullptr) != 1) {
            EVP_MD_CTX_free(ctx);
            return "";
        }

        if (EVP_DigestUpdate(ctx, input.data(), input.size()) != 1) {
            EVP_MD_CTX_free(ctx);
            return "";
        }

        if (EVP_DigestFinal_ex(ctx, hash, &len) != 1) {
            EVP_MD_CTX_free(ctx);
            return "";
        }

        EVP_MD_CTX_free(ctx);

        std::ostringstream oss;
        for (unsigned int i = 0; i < len; ++i) {
            oss << std::hex
                << std::setw(2)
                << std::setfill('0')
                << static_cast<int>(hash[i]);
        }

        return oss.str();
    }
};