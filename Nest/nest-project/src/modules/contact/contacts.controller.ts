import { Body, Controller, Delete, Get, Param, Post, Res, Render } from '@nestjs/common';
import CreateContactDto from "../../dto/create-contact.dto";
import Contact from './contact.entity';
import { ContactsService } from './contacts.service';
import { Response } from 'express';
import { identity, async } from 'rxjs';
import { create } from 'domain';

let handleMessage = function (contact) {
  let hasContact = true;
  if (typeof contact === 'undefined') {
    hasContact = false;
    return { hasContact: hasContact }
  }
  else {
    return {
      firstName: contact.firstName,
      lastName: contact.lastName,
      phoneNumber: contact.phoneNumber,
      isActive: contact.isActive,
      hasContact: hasContact,
    }
  }
}

@Controller('contacts')
export class ContactsController {
  constructor(private readonly contactsService: ContactsService) { }

  @Get()
  @Render('contacts/all_contacts')
  async findAll() {
    const contacts = await this.contactsService.findAll();
    return { contactsList: contacts }
  }

  @Post('create')
  @Render('contacts/create_contact')
  async create(@Body() createContactDto: CreateContactDto): Promise<Contact> {
    return await this.contactsService.insert(createContactDto);
  }

  @Get('create')
  @Render('contacts/create_contact')

  @Get(':id')
  @Render('contacts/contact_by_id')
  async find_by_id(@Param('id') id: string) {
    const contact = await this.contactsService.findOne(id);
    return handleMessage(contact);
  }

  @Get('delete')
  @Render('contacts/delete_contact')

  @Delete('delete/:id')
  @Render('contacts/delete_contact')
  async remove(@Param('id') id: string) {
    const contact = await this.contactsService.findOne(id);
    await this.contactsService.remove(id);
    return handleMessage(contact);
  }
}
