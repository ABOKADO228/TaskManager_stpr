#include <string>
template <typename TId = std::string>
class IDeleteService {
	virtual ~IDeleteService() = default;
	virtual bool remove(const TId& id) = 0;
};