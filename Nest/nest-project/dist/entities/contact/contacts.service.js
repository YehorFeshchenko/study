"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __param = (this && this.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.ContactsService = void 0;
const common_1 = require("@nestjs/common");
const typeorm_1 = require("@nestjs/typeorm");
const typeorm_2 = require("typeorm");
const contact_entity_1 = require("./contact.entity");
let ContactsService = class ContactsService {
    constructor(contactsRepository) {
        this.contactsRepository = contactsRepository;
    }
    getViewName() {
        return 'contact_by_id';
    }
    findAll() {
        return this.contactsRepository.find();
    }
    findOne(id) {
        return this.contactsRepository.findOne(id);
    }
    async insert(contactDetails) {
        const contact = contact_entity_1.default.create();
        const { firstName, lastName, phoneNumber, isActive } = contactDetails;
        contact.firstName = firstName;
        contact.lastName = lastName;
        contact.phoneNumber = phoneNumber;
        contact.isActive = isActive;
        await contact_entity_1.default.save(contact);
        return contact;
    }
    async remove(id) {
        await this.contactsRepository.delete(id);
    }
};
ContactsService = __decorate([
    common_1.Injectable(),
    __param(0, typeorm_1.InjectRepository(contact_entity_1.default)),
    __metadata("design:paramtypes", [typeorm_2.Repository])
], ContactsService);
exports.ContactsService = ContactsService;
//# sourceMappingURL=contacts.service.js.map