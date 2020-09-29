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
exports.ContactsController = void 0;
const common_1 = require("@nestjs/common");
const create_contact_dto_1 = require("../../dto/create-contact.dto");
const contacts_service_1 = require("./contacts.service");
let handleMessage = function (contact) {
    let hasContact = true;
    if (typeof contact === 'undefined') {
        hasContact = false;
        return { hasContact: hasContact };
    }
    else {
        return {
            firstName: contact.firstName,
            lastName: contact.lastName,
            phoneNumber: contact.phoneNumber,
            address: contact.address,
            username: contact.username,
            email: contact.email,
            hasContact: hasContact,
        };
    }
};
let ContactsController = class ContactsController {
    constructor(contactsService) {
        this.contactsService = contactsService;
    }
    async findAll() {
        const contacts = await this.contactsService.findAll();
        return { contactsList: contacts };
    }
    async create(createContactDto) {
        return await this.contactsService.insert(createContactDto);
    }
    async find_by_id(id) {
        const contact = await this.contactsService.findOne(id);
        return handleMessage(contact);
    }
    creating() { }
    async remove(id) {
        const contact = await this.contactsService.findOne(id);
        await this.contactsService.remove(id);
        return handleMessage(contact);
    }
};
__decorate([
    common_1.Get(),
    common_1.Render('contacts/all_contacts'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], ContactsController.prototype, "findAll", null);
__decorate([
    common_1.Post('create'),
    common_1.Render('contacts/create_contact'),
    __param(0, common_1.Body()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [create_contact_dto_1.default]),
    __metadata("design:returntype", Promise)
], ContactsController.prototype, "create", null);
__decorate([
    common_1.Get('get/:id'),
    common_1.Render('contacts/contact_by_id'),
    __param(0, common_1.Param('id')),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [String]),
    __metadata("design:returntype", Promise)
], ContactsController.prototype, "find_by_id", null);
__decorate([
    common_1.Get('create'),
    common_1.Render('contacts/create_contact'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", void 0)
], ContactsController.prototype, "creating", null);
__decorate([
    common_1.Get('delete'),
    common_1.Render('contacts/delete_contact'),
    common_1.Delete('delete/:id'),
    common_1.Render('contacts/delete_contact'),
    __param(0, common_1.Param('id')),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [String]),
    __metadata("design:returntype", Promise)
], ContactsController.prototype, "remove", null);
ContactsController = __decorate([
    common_1.Controller('contacts'),
    __metadata("design:paramtypes", [contacts_service_1.ContactsService])
], ContactsController);
exports.ContactsController = ContactsController;
//# sourceMappingURL=contacts.controller.js.map