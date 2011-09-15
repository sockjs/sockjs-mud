var rabbitUrl = function() {
    if (process.env.VCAP_SERVICES) {
        var conf = JSON.parse(process.env.VCAP_SERVICES);
        return conf['rabbitmq-2.4'][0].credentials.url;
    }
    else {
        return "amqp://localhost";
    }
};
exports.amqp_url = rabbitUrl();
exports.port = process.env.VCAP_APP_PORT || 3001;
