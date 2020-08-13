import { Body, Controller, Delete, Get, Param, Post } from '@nestjs/common';
import CreateContactDto from "../../dto/create-contact.dto";
import Contact from './contact.entity';
import { ContactsService } from './contacts.service';

@Controller('contacts')
export class ContactsController {
  constructor(private readonly contactsService: ContactsService) { }

  @Post('post')
  create(@Body() createContactDto: CreateContactDto): Promise<Contact> {
    return this.contactsService.insert(createContactDto);
  }

  @Get()
  findAll(): Promise<Contact[]> {
    return this.contactsService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string): Promise<Contact> {
    return this.contactsService.findOne(id);
  }

  @Delete(':id')
  remove(@Param('id') id: string): Promise<void> {
    return this.contactsService.remove(id);
  }
}