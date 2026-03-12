#pragma once
#include <optional>
template<typename TEntity, typename TUpdateDto>
class IUpdateService
{
public:
    virtual ~IUpdateService() = default;
    virtual std::optional<TEntity> update(const TUpdateDto& dto) = 0;
};