import { Body, Controller, Delete, Get, Param, Post, Res } from '@nestjs/common';
import CreateContactDto from "../../dto/create-contact.dto";
import Contact from './contact.entity';
import { ContactsService } from './contacts.service';
import { Response } from 'express';
import { identity } from 'rxjs';

@Controller('contacts')
export class ContactsController {
  constructor(private readonly contactsService: ContactsService) { }

  @Post('create')
  create(@Body() createContactDto: CreateContactDto): Promise<Contact> {
    return this.contactsService.insert(createContactDto);
  }

  @Get()
  findAll(): Promise<Contact[]> {
    return this.contactsService.findAll();
  }

  /*@Get(':id')
  findOne(@Param('id') id: string): Promise<Contact> {
    return this.contactsService.findOne(id);
  }*/

  @Get(':id')
  find_by_id(@Res() res: Response, @Param('id') id: string) {
    const contact: Promise<Contact> = this.contactsService.findOne(id);
    return res.render(
      this.contactsService.getViewName(),
      {
        message: 'Hello world!',
        contact_first_name: contact.then(function (contact_new) {
          return contact_new.firstName;
        }).catch(function (reason) {
          return reason;
        }),
      },
    );
  }

  @Delete(':id')
  remove(@Param('id') id: string): Promise<void> {
    return this.contactsService.remove(id);
  }
}