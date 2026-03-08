#pragma once
#include <string>
#include <optional>
template<typename TEntity, typename TId = std::string>
class IGetByIdService
{
public:
    virtual ~IGetByIdService() = default;
    virtual std::optional<TEntity> getById(const TId& id) = 0;
};