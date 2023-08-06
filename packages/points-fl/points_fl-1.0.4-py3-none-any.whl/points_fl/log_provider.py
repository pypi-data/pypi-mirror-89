from points_fl.base import Base, optimization_response
from points_fl.proto import log_provider_pb2


class LogProvider(Base):

    @optimization_response
    def get_last_lines(self, line_num, service_choice):
            return self._log_provider_stub.GetLastLines(log_provider_pb2.GetLastLinesRequest(line_num=line_num, service_choice=service_choice, token=self._token))

    @optimization_response
    def get_log_by_job_i_d(self, job_id):
            return self._log_provider_stub.GetLogByJobID(log_provider_pb2.GetLogByJobIDRequest(job_id=job_id, token=self._token))
