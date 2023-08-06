from videoflow_factory import videoflow_factory
import os

od_flow_config = os.path.abspath("./od_flow.yaml")

od_flow = videoflow_factory(od_flow_config)()

od_flow.run()
od_flow.join()
