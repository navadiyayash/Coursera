const { model, Schema } = require('mongoose');

const criminal_detailSchema = new Schema({
    criminal_name: String,
    criminal_type: String,
    captured_area: String,
    latitude: String,
    longitude: String,
    //  time_stemp: String, 
     occurances: String 
});

module.exports = model('Criminal_detail', criminal_detailSchema);

