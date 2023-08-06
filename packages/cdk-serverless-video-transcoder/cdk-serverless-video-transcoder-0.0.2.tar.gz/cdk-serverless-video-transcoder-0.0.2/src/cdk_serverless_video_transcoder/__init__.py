"""
# my project
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_ec2
import aws_cdk.aws_s3
import aws_cdk.core


class VideoTranscoder(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-serverless-video-transcoder.VideoTranscoder",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        bucket: typing.Optional[aws_cdk.aws_s3.Bucket] = None,
        lambda_memory_size: typing.Optional[jsii.Number] = None,
        lambda_time_out: typing.Optional[jsii.Number] = None,
        parallel_group_no: typing.Optional[jsii.Number] = None,
        segment_time: typing.Optional[jsii.Number] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param bucket: 
        :param lambda_memory_size: 
        :param lambda_time_out: 
        :param parallel_group_no: 
        :param segment_time: 
        :param vpc: 
        """
        props = VideoTranscoderProp(
            bucket=bucket,
            lambda_memory_size=lambda_memory_size,
            lambda_time_out=lambda_time_out,
            parallel_group_no=parallel_group_no,
            segment_time=segment_time,
            vpc=vpc,
        )

        jsii.create(VideoTranscoder, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="videoBucket")
    def video_bucket(self) -> aws_cdk.aws_s3.Bucket:
        return jsii.get(self, "videoBucket")


@jsii.data_type(
    jsii_type="cdk-serverless-video-transcoder.VideoTranscoderProp",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "lambda_memory_size": "lambdaMemorySize",
        "lambda_time_out": "lambdaTimeOut",
        "parallel_group_no": "parallelGroupNo",
        "segment_time": "segmentTime",
        "vpc": "vpc",
    },
)
class VideoTranscoderProp:
    def __init__(
        self,
        *,
        bucket: typing.Optional[aws_cdk.aws_s3.Bucket] = None,
        lambda_memory_size: typing.Optional[jsii.Number] = None,
        lambda_time_out: typing.Optional[jsii.Number] = None,
        parallel_group_no: typing.Optional[jsii.Number] = None,
        segment_time: typing.Optional[jsii.Number] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param bucket: 
        :param lambda_memory_size: 
        :param lambda_time_out: 
        :param parallel_group_no: 
        :param segment_time: 
        :param vpc: 
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if bucket is not None:
            self._values["bucket"] = bucket
        if lambda_memory_size is not None:
            self._values["lambda_memory_size"] = lambda_memory_size
        if lambda_time_out is not None:
            self._values["lambda_time_out"] = lambda_time_out
        if parallel_group_no is not None:
            self._values["parallel_group_no"] = parallel_group_no
        if segment_time is not None:
            self._values["segment_time"] = segment_time
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def bucket(self) -> typing.Optional[aws_cdk.aws_s3.Bucket]:
        result = self._values.get("bucket")
        return result

    @builtins.property
    def lambda_memory_size(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("lambda_memory_size")
        return result

    @builtins.property
    def lambda_time_out(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("lambda_time_out")
        return result

    @builtins.property
    def parallel_group_no(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("parallel_group_no")
        return result

    @builtins.property
    def segment_time(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("segment_time")
        return result

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        result = self._values.get("vpc")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VideoTranscoderProp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "VideoTranscoder",
    "VideoTranscoderProp",
]

publication.publish()
