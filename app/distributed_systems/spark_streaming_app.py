"""
./bin/spark-submit --conf spark.driver.allowMultipleContexts=true --conf spark.driver.extraJavaOptions=-Dlog4j.configuration=log4j-spark.properties --conf spark.executor.extraJavaOptions=-Dlog4j.configuration=log4j-spark.properties --master 'local[2]' --class com.krux.spark.streaming.jobs.PixelStreamProcessor /Users/ssatish/git/krux-spark-streaming/spark-streaming/target/scala-2.11/krux-spark-streaming-assembly-0.0.1.jar
"""