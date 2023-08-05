#pragma once
#include "TopicModel.hpp"

namespace tomoto
{
    enum class TermWeight { one, idf, pmi, size };

	template<typename _Scalar>
	struct ShareableVector : Eigen::Map<Eigen::Matrix<_Scalar, -1, 1>>
	{
		Eigen::Matrix<_Scalar, -1, 1> ownData;
		ShareableVector(_Scalar* ptr = nullptr, Eigen::Index len = 0) 
			: Eigen::Map<Eigen::Matrix<_Scalar, -1, 1>>(nullptr, 0)
		{
			init(ptr, len);
		}

		void init(_Scalar* ptr, Eigen::Index len)
		{
			if (!ptr && len)
			{
				ownData = Eigen::Matrix<_Scalar, -1, 1>::Zero(len);
				ptr = ownData.data();
			}
			// is this the best way??
			this->m_data = ptr;
			((Eigen::internal::variable_if_dynamic<Eigen::Index, -1>*)&this->m_rows)->setValue(len);
		}

		void conservativeResize(size_t newSize)
		{
			ownData.conservativeResize(newSize);
			init(ownData.data(), ownData.size());
		}

		void becomeOwner()
		{
			if (ownData.data() != this->m_data)
			{
				ownData = *this;
				init(ownData.data(), ownData.size());
			}
		}
	};

	template<typename _Base, TermWeight _tw>
	struct SumWordWeight
	{
		Float sumWordWeight = 0;
		Float getSumWordWeight() const
		{
			return sumWordWeight;
		}

		void updateSumWordWeight(size_t realV)
		{
			sumWordWeight = std::accumulate(static_cast<_Base*>(this)->wordWeights.begin(), static_cast<_Base*>(this)->wordWeights.end(), 0.f);
		}
	};

	template<typename _Base>
	struct SumWordWeight<_Base, TermWeight::one>
	{
		int32_t sumWordWeight = 0;
		int32_t getSumWordWeight() const
		{
			return sumWordWeight;
		}

		void updateSumWordWeight(size_t realV)
		{
			sumWordWeight = std::count_if(static_cast<_Base*>(this)->words.begin(), static_cast<_Base*>(this)->words.end(), [realV](Vid w)
			{
				return w < realV;
			});
		}
	};

	template<TermWeight _tw>
	struct DocumentLDA : public DocumentBase, SumWordWeight<DocumentLDA<_tw>, _tw>
	{
	public:
		using DocumentBase::DocumentBase;
		using WeightType = typename std::conditional<_tw == TermWeight::one, int32_t, float>::type;

		tvector<Tid> Zs;
		tvector<Float> wordWeights;
		ShareableVector<WeightType> numByTopic;

		DEFINE_SERIALIZER_AFTER_BASE_WITH_VERSION(DocumentBase, 0, Zs, wordWeights);
		DEFINE_TAGGED_SERIALIZER_AFTER_BASE_WITH_VERSION(DocumentBase, 1, 0x00010001, Zs, wordWeights);

		template<typename _TopicModel> void update(WeightType* ptr, const _TopicModel& mdl);
		
		WeightType getWordWeight(size_t idx) const
		{
			return _tw == TermWeight::one ? 1 : wordWeights[idx];
		}

		std::vector<Float> getCountVector(size_t V) const
		{
			std::vector<Float> vs(V);
			for (size_t i = 0; i < words.size(); ++i)
			{
				if (words[i] >= V) continue;
				vs[words[i]] += wordWeights.empty() ? 1.f : wordWeights[i];
			}
			return vs;
		}
	};

    class ILDAModel : public ITopicModel
	{
	public:
		using DefaultDocType = DocumentLDA<TermWeight::one>;
		static ILDAModel* create(TermWeight _weight, size_t _K = 1, 
			Float _alpha = 0.1, Float _eta = 0.01, size_t seed = std::random_device{}(),
			bool scalarRng = false);

		virtual TermWeight getTermWeight() const = 0;
		virtual size_t getOptimInterval() const = 0;
		virtual void setOptimInterval(size_t) = 0;
		virtual size_t getBurnInIteration() const = 0;
		virtual void setBurnInIteration(size_t) = 0;
		virtual std::vector<uint64_t> getCountByTopic() const = 0;
		virtual Float getAlpha() const = 0;
		virtual Float getAlpha(size_t k) const = 0;
		virtual Float getEta() const = 0;

		virtual std::vector<Float> getWordPrior(const std::string& word) const = 0;
		virtual void setWordPrior(const std::string& word, const std::vector<Float>& priors) = 0;
	};
}
