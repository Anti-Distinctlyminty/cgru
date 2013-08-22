#include "mctaskup.h"

#include <stdio.h>
#include <memory.h>

#include "../msg.h"

#define AFOUTPUT
#undef AFOUTPUT
#include "../../include/macrooutput.h"

using namespace af;

MCTaskUp::MCTaskUp
(
	int clientId,

	int numJob,
	int numBlock,
	int numTask,
	int number,

	int UpStatus,
	int UpPercent,
	int UpFrame,
	int UpPercentFrame,
	std::string activity,
	int dataLen,
	char * data
):
	m_clientid      ( clientId),

	m_numjob        ( numJob),
	m_numblock      ( numBlock),
	m_numtask       ( numTask),
	m_number        ( number),

	m_status        ( UpStatus),
	m_percent       ( UpPercent),
	m_frame         ( UpFrame),
	m_percent_frame ( UpPercentFrame),
	m_activity      ( activity),

	m_datalen       ( dataLen ),
	m_data          ( data ),
	m_deleteData    ( false), // Don not delete data on client side, as it is not copied

	m_files_num(0),
	m_files_data( NULL)
{
}

MCTaskUp::MCTaskUp( Msg * msg):
	m_data ( NULL),
	m_files_data( NULL),
	m_deleteData( true)       // Delete data on server side, as it was allocated and copied from incoming message
{
	read( msg);
}

MCTaskUp::~MCTaskUp()
{
	if( m_deleteData && m_data ) delete [] m_data;
	if( m_files_data ) delete [] m_files_data;
}

void MCTaskUp::v_readwrite( Msg * msg)
{
	rw_int32_t( m_clientid,       msg);

	rw_int32_t( m_numjob,         msg);
	rw_int32_t( m_numblock,       msg);
	rw_int32_t( m_numtask,        msg);
	rw_int32_t( m_number,         msg);

	rw_int8_t ( m_status,         msg);
	rw_int8_t ( m_percent,        msg);
	rw_int32_t( m_frame,          msg);
	rw_int8_t ( m_percent_frame,  msg);
	rw_String ( m_activity,       msg);
	rw_int32_t( m_datalen,        msg);
	rw_int32_t( m_files_num,      msg);

	if( m_datalen )
		rwData( msg);

	if( m_files_num )
		rwFiles( msg);
}

void MCTaskUp::rwData( Msg * msg)
{
	if( msg->isWriting() )
	{
		if( m_data == NULL )
		{
			AFERROR("MCTaskUp::readwrite: data == NULL.")
			return;
		}
	}
	else
	{
		m_data = new char[m_datalen];
		if( m_data == NULL )
		{
			AFERROR("MCTaskUp::readwrite: Can't allocate memory for data.")
			m_datalen = 0;
			return;
		}
	}
	rw_data( m_data, msg, m_datalen);
}

void MCTaskUp::rwFiles( Msg * msg)
{
	rw_int32_t(    m_files_data_len, msg);
	rw_Int32_Vect( m_files_sizes,    msg);
	rw_StringVect( m_files_names,    msg);
	if( msg->isReading())
		m_files_data = new char[m_files_data_len];
	rw_data( m_files_data, msg, m_files_data_len);
}

void MCTaskUp::addFile( const std::string & i_name, const char * i_data, int i_size)
{
	if( m_files_data == NULL )
	{
		// This is the first added file:
		m_files_data_buflen = i_size * 4;
		m_files_data = new char[ m_files_data_buflen];
		m_files_data_len = 0;
	}
	else if( m_files_data_buflen < ( m_files_data_len + i_size ))
	{
		// New file will not fit in buffer:
		char * old_buffer = m_files_data;
		m_files_data_buflen += i_size * 4;
		m_files_data = new char[m_files_data_buflen];
		memcpy( m_files_data, old_buffer, m_files_data_len);
		delete [] old_buffer;
	}

	m_files_num++;
	m_files_sizes.push_back( i_size);
	m_files_names.push_back( i_name);
	memcpy( m_files_data + m_files_data_len, i_data, i_size);
	m_files_data_len += i_size;
}

const char * MCTaskUp::getFileData( int i_num) const
{
	if( i_num >= m_files_num )
	{
		AFERROR("MCTaskUp::getFileData: i_num >= m_files_num")
		return NULL;
	}
	if( m_files_data == NULL )
	{
		AFERROR("MCTaskUp::getFileData: m_files_data == NULL")
		return NULL;
	}

	int offset = 0;
	for( int i = 0; i < i_num; i++)
		offset += m_files_sizes[i];
	
	return m_files_data + offset;
}

void MCTaskUp::v_generateInfoStream( std::ostringstream & stream, bool full) const
{
	if( full )
	{
		stream << "TaskUp: client=" << m_clientid
			<< ", job="      << m_numjob
			<< ", block="    << m_numblock
			<< ", task="     << m_numtask
			<< ", number="   << m_number
			<< ", activity=" << m_activity
			<< ", datalen="  << m_datalen
			<< ", files="    << m_files_num
			<< ", status="   << int(m_status)
			<< ", percent="  << int(m_percent);
		if( m_datalen && m_data) stream << "data:\n" << std::string( m_data, m_datalen) << std::endl;
	}
	else
	{
		stream << "TaskUp:"
			<< " C" << m_clientid
			<< " J" << m_numjob
			<< " B" << m_numblock
			<< " T" << m_numtask
			<< " #" << m_number
			<< " A" << m_activity
			<< " D" << m_datalen
			<< " F" << m_files_num
			<< " S" << int(m_status)
			<< " "  << int(m_percent) << "%";
	}
}

