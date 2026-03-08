#pragma once
#include <vector>

template<typename TEntity>
class IGetAllService
{
public:
    virtual ~IGetAllService() = default;
    virtual std::vector<TEntity> getAll() = 0;
};