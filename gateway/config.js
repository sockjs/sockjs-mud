var rabbitUrl = function() {
    if (process.env.VCAP_SERVICES) {
        var conf = JSON.parse(process.env.VCAP_SERVICES);
        return conf['rabbitmq-2.4'][0].credentials.url;
    } else if(process.env.RABBITMQ_URL) {
        return process.env.RABBITMQ_URL;
    } else {
        return "amqp://localhost";
    }
};
exports.amqp_url = rabbitUrl();
exports.port = process.env.VCAP_APP_PORT || process.env.PORT || 3001;
