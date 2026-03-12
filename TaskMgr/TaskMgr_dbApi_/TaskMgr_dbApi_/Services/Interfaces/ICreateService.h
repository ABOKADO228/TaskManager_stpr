template<typename TEntity, typename TCreateDto>
class ICreateService
{
public:
    virtual ~ICreateService() = default;
    virtual TEntity create(const TCreateDto& dto) = 0;
};