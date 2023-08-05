﻿/*
* Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
*
* Licensed under the Apache License, Version 2.0 (the "License").
* You may not use this file except in compliance with the License.
* A copy of the License is located at
*
*  http://aws.amazon.com/apache2.0
*
* or in the "license" file accompanying this file. This file is distributed
* on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
* express or implied. See the License for the specific language governing
* permissions and limitations under the License.
*/

#pragma once
#include <aws/s3/S3_EXPORTS.h>
#include <aws/core/utils/memory/stl/AWSString.h>
#include <aws/core/utils/memory/stl/AWSVector.h>
#include <aws/s3/model/MetricsConfiguration.h>
#include <utility>

namespace Aws
{
template<typename RESULT_TYPE>
class AmazonWebServiceResult;

namespace Utils
{
namespace Xml
{
  class XmlDocument;
} // namespace Xml
} // namespace Utils
namespace S3
{
namespace Model
{
  class AWS_S3_API ListBucketMetricsConfigurationsResult
  {
  public:
    ListBucketMetricsConfigurationsResult();
    ListBucketMetricsConfigurationsResult(const Aws::AmazonWebServiceResult<Aws::Utils::Xml::XmlDocument>& result);
    ListBucketMetricsConfigurationsResult& operator=(const Aws::AmazonWebServiceResult<Aws::Utils::Xml::XmlDocument>& result);


    /**
     * <p>Indicates whether the returned list of metrics configurations is complete. A
     * value of true indicates that the list is not complete and the
     * NextContinuationToken will be provided for a subsequent request.</p>
     */
    inline bool GetIsTruncated() const{ return m_isTruncated; }

    /**
     * <p>Indicates whether the returned list of metrics configurations is complete. A
     * value of true indicates that the list is not complete and the
     * NextContinuationToken will be provided for a subsequent request.</p>
     */
    inline void SetIsTruncated(bool value) { m_isTruncated = value; }

    /**
     * <p>Indicates whether the returned list of metrics configurations is complete. A
     * value of true indicates that the list is not complete and the
     * NextContinuationToken will be provided for a subsequent request.</p>
     */
    inline ListBucketMetricsConfigurationsResult& WithIsTruncated(bool value) { SetIsTruncated(value); return *this;}


    /**
     * <p>The marker that is used as a starting point for this metrics configuration
     * list response. This value is present if it was sent in the request.</p>
     */
    inline const Aws::String& GetContinuationToken() const{ return m_continuationToken; }

    /**
     * <p>The marker that is used as a starting point for this metrics configuration
     * list response. This value is present if it was sent in the request.</p>
     */
    inline void SetContinuationToken(const Aws::String& value) { m_continuationToken = value; }

    /**
     * <p>The marker that is used as a starting point for this metrics configuration
     * list response. This value is present if it was sent in the request.</p>
     */
    inline void SetContinuationToken(Aws::String&& value) { m_continuationToken = std::move(value); }

    /**
     * <p>The marker that is used as a starting point for this metrics configuration
     * list response. This value is present if it was sent in the request.</p>
     */
    inline void SetContinuationToken(const char* value) { m_continuationToken.assign(value); }

    /**
     * <p>The marker that is used as a starting point for this metrics configuration
     * list response. This value is present if it was sent in the request.</p>
     */
    inline ListBucketMetricsConfigurationsResult& WithContinuationToken(const Aws::String& value) { SetContinuationToken(value); return *this;}

    /**
     * <p>The marker that is used as a starting point for this metrics configuration
     * list response. This value is present if it was sent in the request.</p>
     */
    inline ListBucketMetricsConfigurationsResult& WithContinuationToken(Aws::String&& value) { SetContinuationToken(std::move(value)); return *this;}

    /**
     * <p>The marker that is used as a starting point for this metrics configuration
     * list response. This value is present if it was sent in the request.</p>
     */
    inline ListBucketMetricsConfigurationsResult& WithContinuationToken(const char* value) { SetContinuationToken(value); return *this;}


    /**
     * <p>The marker used to continue a metrics configuration listing that has been
     * truncated. Use the NextContinuationToken from a previously truncated list
     * response to continue the listing. The continuation token is an opaque value that
     * Amazon S3 understands.</p>
     */
    inline const Aws::String& GetNextContinuationToken() const{ return m_nextContinuationToken; }

    /**
     * <p>The marker used to continue a metrics configuration listing that has been
     * truncated. Use the NextContinuationToken from a previously truncated list
     * response to continue the listing. The continuation token is an opaque value that
     * Amazon S3 understands.</p>
     */
    inline void SetNextContinuationToken(const Aws::String& value) { m_nextContinuationToken = value; }

    /**
     * <p>The marker used to continue a metrics configuration listing that has been
     * truncated. Use the NextContinuationToken from a previously truncated list
     * response to continue the listing. The continuation token is an opaque value that
     * Amazon S3 understands.</p>
     */
    inline void SetNextContinuationToken(Aws::String&& value) { m_nextContinuationToken = std::move(value); }

    /**
     * <p>The marker used to continue a metrics configuration listing that has been
     * truncated. Use the NextContinuationToken from a previously truncated list
     * response to continue the listing. The continuation token is an opaque value that
     * Amazon S3 understands.</p>
     */
    inline void SetNextContinuationToken(const char* value) { m_nextContinuationToken.assign(value); }

    /**
     * <p>The marker used to continue a metrics configuration listing that has been
     * truncated. Use the NextContinuationToken from a previously truncated list
     * response to continue the listing. The continuation token is an opaque value that
     * Amazon S3 understands.</p>
     */
    inline ListBucketMetricsConfigurationsResult& WithNextContinuationToken(const Aws::String& value) { SetNextContinuationToken(value); return *this;}

    /**
     * <p>The marker used to continue a metrics configuration listing that has been
     * truncated. Use the NextContinuationToken from a previously truncated list
     * response to continue the listing. The continuation token is an opaque value that
     * Amazon S3 understands.</p>
     */
    inline ListBucketMetricsConfigurationsResult& WithNextContinuationToken(Aws::String&& value) { SetNextContinuationToken(std::move(value)); return *this;}

    /**
     * <p>The marker used to continue a metrics configuration listing that has been
     * truncated. Use the NextContinuationToken from a previously truncated list
     * response to continue the listing. The continuation token is an opaque value that
     * Amazon S3 understands.</p>
     */
    inline ListBucketMetricsConfigurationsResult& WithNextContinuationToken(const char* value) { SetNextContinuationToken(value); return *this;}


    /**
     * <p>The list of metrics configurations for a bucket.</p>
     */
    inline const Aws::Vector<MetricsConfiguration>& GetMetricsConfigurationList() const{ return m_metricsConfigurationList; }

    /**
     * <p>The list of metrics configurations for a bucket.</p>
     */
    inline void SetMetricsConfigurationList(const Aws::Vector<MetricsConfiguration>& value) { m_metricsConfigurationList = value; }

    /**
     * <p>The list of metrics configurations for a bucket.</p>
     */
    inline void SetMetricsConfigurationList(Aws::Vector<MetricsConfiguration>&& value) { m_metricsConfigurationList = std::move(value); }

    /**
     * <p>The list of metrics configurations for a bucket.</p>
     */
    inline ListBucketMetricsConfigurationsResult& WithMetricsConfigurationList(const Aws::Vector<MetricsConfiguration>& value) { SetMetricsConfigurationList(value); return *this;}

    /**
     * <p>The list of metrics configurations for a bucket.</p>
     */
    inline ListBucketMetricsConfigurationsResult& WithMetricsConfigurationList(Aws::Vector<MetricsConfiguration>&& value) { SetMetricsConfigurationList(std::move(value)); return *this;}

    /**
     * <p>The list of metrics configurations for a bucket.</p>
     */
    inline ListBucketMetricsConfigurationsResult& AddMetricsConfigurationList(const MetricsConfiguration& value) { m_metricsConfigurationList.push_back(value); return *this; }

    /**
     * <p>The list of metrics configurations for a bucket.</p>
     */
    inline ListBucketMetricsConfigurationsResult& AddMetricsConfigurationList(MetricsConfiguration&& value) { m_metricsConfigurationList.push_back(std::move(value)); return *this; }

  private:

    bool m_isTruncated;

    Aws::String m_continuationToken;

    Aws::String m_nextContinuationToken;

    Aws::Vector<MetricsConfiguration> m_metricsConfigurationList;
  };

} // namespace Model
} // namespace S3
} // namespace Aws
