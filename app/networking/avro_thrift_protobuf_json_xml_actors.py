"""
Martin Kleppman - Big Ideas Behind Reliable, Scalable and Maintainable Systems
Chapter 4 - ENCODING, DATA FORMATS AND SCHEMA EVOLUTION -

1) Design for evolvability - Support rolling upgrades of services on a cluster, in a phased manner
without downtime. So some nodes maybe updated first before others. Old and new code as well as old
and new data formats may all co-exist on a cluster at the same time. Adjacent versions (of code and
data formats) have to be both forwards compatible as well as backwards compatible.

2) When you want to WR data to a file or send it over the N/W, pointers of data structures (like
trees, hash-map, etc) dont make sense. It has to be encoded as a self-contained sequence of bytes.
A pointer doesn't make sense to any other process.
    Encoding to byte stream is also called serialization, marshalling, pickling. Decoding from byte
stream to in-memory object representation is called decoding, deserialization, unmarshalling, etc.

Some language-specific in-built encoding formats are -
    Java - java.io.Serializable
    Python - pickle
    Ruby - marshall
    java 3rd party lib - Kryo

Disadvantage of all the above:
    a) Language-specific. No cross-language support.

    b) Decoding process often has to be able to instantiate arbitrary classes. This is a security
    vulnerability if an attacker can send a byte stream which can decode to a malicious Class.

    c) Java serialization is notorious for its bloated size and CPU cycles required to encode (
    a lot => inefficient).

    d) Inconvenient problems of forward & backward incompatibility are ignored.

3) JSON, XML and CSV are text formats, human-readable.
    a) But XML and CSV dont distinguish b/w numbers and strings.

    b) JSON does, but it doesnt distinguish between int and float nor handle precision. This can be
    a problem for integers > 2^53 as they cannot be exactly represented by IEEE 754 double-precision
    floating-point format. Tweet_ids are a 64-bit int, so javascript applications may have problems
    with it. Hence, JSON returned by twitter's API includes tweet_id twice - once as JSON number,
    and another as a decimal string.

    c) Unicode support is good in both JSON and XML, but both dont support binary strings (seq of
    bytes w/o char-encoding). Binary strings are a useful feature, so people get around this
    limitation by encoding the binary data as text using Base64. The schema is then used to indicate
    that the value should be interpreted as Base64-encoded. This works, but its somewhat hacky and
    increases the data size by 33%.

4) Thrift: It has 2 separate binary encodings - BinaryProtocol and CompactProtocol.
In thrift, there is `list` datatype thats parametrized with datatype of list elements.

    Disadv - This does not allow schema evolution from single-valued column to array/list. Protobuf
    allows it.

    Adv - This however, allows for nested lists.

5) Avro also uses a schema to specify the structure of the data being encoded. It has two
schema languages: one (Avro IDL) intended for human editing, and one (based on
JSON) that is more easily machine-readable.
    a) Avro encoding is the most compact of all and doesnt have field tag_ids unlike thrift or
    protobuf.

    b) For forward an dbackward compatibility between reader & writer schemas, when adding or
    removing columns, they should always have a default value. `Null` is explicitly specified as a
    `union` type to prevent bugs. There's no `required` and `optional` fields unlike thrift and
    protobuf.

    c) For IPC (inter-process communication over a N/W), can negotiate the avro schema version on
    connection setup and then use that schema for the lifetime of the connection. The Avro RPC
    protocol works this way.

    d) Avro is friendlier to dynamically generated schemas than protobuf or thrift. Eg - If DB DDL
    changes, can take new avro schema dump instead of manually reassigning tag_ids in protobuf or
    thrift which is error prone. We can then encode the database contents using that avro schema,
    dumping it all to an `Avro object container file`.

    This property is especially useful in conjunction with dynamically typed data processing
    languages like Apache Pig. In Pig, you can just open some Avro files, start analyzing them, and
    write derived datasets to output files in Avro format without even thinking about schemas.

    LinkedIn's document database Espresso (like MongoDB) uses Avro for storage, allowing it to use
    Avro's schema evolution rules
------------------------------------------------------------------------------------------------
DATA FLOW BETWEEN PROCESSES - can happen in 3 ways. Data outlives code in enterprises.

1) Thru DBs

2) Thru services - REST & RPC -
    a) A client-side javascript application running inside a web browser can make an XmlHttpRequest
    to become a Http client. This technique is called Ajax.

    b) When HTTP is used as the underlying protocol for talking to the service, it is called a
    web service.

    c) Within the same data center, different services talking to each other in a microservice
    architecture is sometimes called as middleware.

    d) RESTful APIs tend to favor simpler approaches, typically involving less code generation
    and automated tooling (=> more human readable). Swagger is a definition format to generate
    documentation about RESTful APIs. They also use the HTTP protocol for things like caching, etc

    e) Thrift and Avro come with RPC support included, gRPC is an RPC implementation using
    Protocol Buffers, Finagle also uses Thrift, and Rest.li uses JSON over HTTP.

    f) Finagle and Rest.li use futures (promises) to encapsulate asynchronous actions that may fail.
    Futures also simplify situations where you need to make requests to multiple services in
    parallel, and combine their results. gRPC supports streams, where a call consists of not just
    one request and one response, but a series of requests and responses over time.

    g) By design, the gRPC protocol cannot be transported over HTTP. The gRPC protocol mandates HTTP/2 in order to take
    advantage of the multiplexing and streaming features of an HTTP/2 connection.

    h) Some of these frameworks also provide "service discovery" - that is, allowing a client to
    find out at which IP address and port number it can find a particular service.

    i) There are vast set of tools available for REST - servers, caches, load balancers, proxies,
    firewalls, monitoring, debugging tools, testing tools, `curl`, web browsers, multi-language
    support for REST.

    j) It is reasonable to assume that all the servers will be updated first, and all the clients
    second. Thus, you only need backward compatibility on requests, and forward compatibility on
    responses

3) Thru async msg passing - There are 2 types here - msg brokers (eg - Kafka) vs distributed actor
frameworks
    Msg transmission occurs via an intermediary like actor or msg broker. Similar to DBs in the
    sense that no direct N/W cnxn exists.

    Has several advantages over RPC as follows -
    a) Acts as buffer if recipient is unavailable or over-loaded. Hence improves reliability.

    b) Can automatically re-deliver msgs to a process that has crashed, thus prevents msgs from
    being lost.

    c) Avoids sender needing to know IP address and port of recipient. This is very useful in cloud
    deployment where virtual m/cs often come and go.

    d) Allows broadcast of 1 msg to several recipients.

    e) Logically decouples sender from receiver.

    This style is asynchronous. Sender doesn't wait for response or for msg to be delivered. It
    sends and forgets.
-------------
    DISTRIBUTED ACTOR FRAMEWORKS -

    a) The actor model is a programming model for concurrency in a single process. Rather than
    dealing directly with threads (and the associated problems of race conditions, locking, and
    deadlock), logic is encapsulated in actors.

    b) Each actor typically represents one client or entity, it may have some local state (which is
    not shared with any other actor), and it communicates with other actors by sending and receiving
    asynchronous messages.

    c) Message delivery is not guaranteed - in certain error scenarios, messages will be lost.
    Since each actor processes only one message at a time, it doesn't need to worry about threads,
    and each actor can be scheduled independently by the framework.

    d) In distributed actor frameworks, this programming model is used to scale an application
    across multiple nodes. The same message-passing mechanism is used, no matter whether the sender
    and recipient are on the same node or different nodes.

    e) If they are on different nodes, the message is transparently encoded into a byte sequence,
    sent over the network, and decoded on the other side.

    f) Location transparency works better in the actor model than in RPC, because the actor model
    already assumes that messages may be lost, even within a single process. Although latency over
    the network is likely higher than within the same process, there is less of a fundamental
    mismatch between local and remote communication when using the actor model.
    -----------
    A distributed actor framework essentially integrates a message broker and the actor
    programming model into a single framework. 3 popular distributed actor frameworks handle msg
    encoding as follows -

    a) Akka - Uses java's in-built serialization by default. This provides no fwd/backward
    compatibility. However, this is replaceable with something like protobuf, thus gaining the
    ability to do rolling upgrades.

    B) Orleans and Erlang OTP (used by whatsApp architecture) are 2 other systems. But schema
    changes and rolling upgrades are hard in these.

"""